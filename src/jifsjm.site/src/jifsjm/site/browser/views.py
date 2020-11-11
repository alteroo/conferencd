import StringIO
import csv

# Form schema and MessageFactory, important!
from zope.interface import Interface
from zope.schema import TextLine
from zope.i18nmessageid import MessageFactory
from plone.i18n.normalizer.interfaces import IIDNormalizer

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces.controlpanel import IMailSchema
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

# Form field imports
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import form, field
from plone.namedfile.field import NamedFile

# Wraps form to View import
from Products.CMFCore.utils import getToolByName
from plone.z3cform.layout import wrap_form
import re


from plone import api

_ = MessageFactory("jifsjm.views")


class IConferenceAttendeeImporterForm(Interface):
    csv_file = NamedFile(title=_(u'Upload CSV containing User Accounts'))

class ConferenceAttendeeImporterForm(form.Form):

    fields = field.Fields(IConferenceAttendeeImporterForm)
    ignoreContext = True
    invalid_emails = []

    def update_widgets(self):
        super(ConferenceAttendeeImporterForm, self).update_widgets()
    
    def process_groups_from_csv(self, fields):
        """
        descr:  Takes values from csv and then adds enabled groups to array
        param:  fields - Fields from csv row
        return: groups - Array of enabled groups
        """
        groups =[]
        if fields['Conference only']:
            groups.append('Conference')
        if fields['Day 1 only']:
            groups.append('Day_1')
        if fields['Day 2 only']:
            groups.append('Day_2')
        if fields['Workshop only']:
            groups.append('Workshop')
        if fields['Conference & Workshop']:
            groups.extend(['Workshop', 'Conference'])
        return groups
    
    def add_groups(self, group, username):
        """
        descr:  Takes group and adds to plone
        param:  group - Specific enabled group
        param:  username - Specific username
        return: null
        """        
        group_exists = api.group.get(groupname=group)
        if not group_exists:
            api.group.create(
                groupname=group,
                roles=['Member',]
            )
        api.group.add_user(groupname=group, username=username)

        
    def add_user(self, fields={},password=None):
        properties = fields
        
        # Format values from csv, removes whitespace and lowercase all fields 
        if not fields['Name of Applicant']:
            return
        else:
            username=fields['Name of Applicant'].strip().replace(" ","").replace("'","").lower()
        
        if fields['E-mail']:
            email = fields['E-mail'].strip().replace(" ", "").lower()
        else:
            email = fields['Name of Applicant'].strip().replace(" ","").lower() + "@conference.com"
        
        # Process groups present in each row
        groups = self.process_groups_from_csv(fields)

        # Use email as username and email field
        try:
            user = api.user.create(
                email=email,
                username=username,
                password=password)
        except ValueError as e:
            userdata = {
                "user": username, 
                "email": email,
                "error": e
            }
            if userdata not in self.invalid_emails:
                self.invalid_emails.append(userdata)
            return None

        for group in groups:
            self.add_groups(group.strip(), username)
        return user
            
    def notify_account_updates(self, member, userdata=None):
        mail_host = api.portal.get_tool(name='MailHost')
        mail_template = ViewPageTemplateFile('mail_imported_users.pt')
        
        registry = getUtility(IRegistry)
        mail_settings = registry.forInterface(IMailSchema, prefix='plone')
        email_from_address = mail_settings.email_from_address
        email_from_name = mail_settings.email_from_name
        encoding = registry.get('plone.email_charset', 'utf-8')
        
        if not member:
            return False
            
        to_email = member.getProperty("email")
        if not to_email:
            self.invalid_emails.append(userdata)
            return False
        
        message = mail_template(
            self,
            member=member,
            portal_url=self.context.absolute_url(),
            charset='utf-8',
            email_from_name=email_from_name,
            email_from_address=email_from_address,
            userdata=userdata)
        message = message.encode(encoding)
        return mail_host.send(
            message,
            mto=to_email,
            mfrom="{}<{}>".format(
                email_from_name,
                email_from_address
            ),
            subject=("JBA/JIFS 6th Annual AML/CFT conference materials"),
            msg_type='text/html',
            immediate=True)
        

    def process_participant(self, row):
        """process a Conference participant"""
        # param name: Column name: 1st row cell content value, header
        out = ""
        fields = {}

        for field_name in self.expected_fieldnames:
            if field_name == "Name of Applicant":
                fields["fullname"] = row[self.index[field_name]]
            fields[field_name] = row[self.index[field_name]]
            
        normalizer = getUtility(IIDNormalizer)
        username_ = normalizer.normalize(fields['Name of Applicant'])
        username = re.sub('[^0-9a-zA-Z]+', '', username_)
        username = re.sub(r'[^\x00-\x7F]+',' ', username)
        
        
        regtool = api.portal.get_tool('portal_registration')
        password = regtool.generatePassword()[:6]
        
        
        # if user is not None:
        user_object = {
            "user": username, 
            "password": password,
            "status" : "",
        }

        user = api.user.get(username=username)
        
        if user:    
            #update password and fields
            user.setSecurityProfile(password=password)
            user.setMemberProperties(mapping=fields)
            status_message = "updated successfully"
            user_object["status"] = status_message
            self.notify_account_updates(member=user, userdata=user_object)
        else:
            user = self.add_user(fields=fields,password=password)
            if user:
                status_message = "imported successfully"
                user_object["status"] = status_message    
                self.notify_account_updates(member=user, userdata=user_object)
        if len(self.invalid_emails) > 0:
            with open('invalid_emails.csv', 'w') as csvfile:
                fieldnames = self.invalid_emails[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
                writer.writeheader()
                writer.writerows(self.invalid_emails)
        return user_object

    def process_csv(self, data):
        # Create object from NamedFile
        io = StringIO.StringIO(data)
        
        # Create csv reader
        reader = csv.reader(io, delimiter=',', dialect="excel", quotechar='"')
        
        self.expected_fieldnames = ['#', 'Organization/Contact Person', 'Name of Applicant', 
                           'Position', 'E-mail', 
                           'Conference only', 'Day 1 only','Day 2 only','Workshop only', 'Conference & Workshop']
        # Skips header images and extra rows in JIFS csv
        for skip in xrange(0,5):    
            reader.next()
            
        header = reader.next()
        header = [fieldname_.strip() for fieldname_ in header]
        self.index = {}
        missing_field_names = []


        for field_name in self.expected_fieldnames:
            if field_name in header:
                self.index[field_name] = header.index(field_name)
            else:
               missing_field_names.append(field_name)

            self.membership = getToolByName(self.context, 'portal_membership')
        importNum = 0
        importSummary = []

        for row in reader:
            importSummary.append(self.process_participant(row))
            importNum += 1

        return dict(number=importNum,groups_created=[])

    @button.buttonAndHandler(u'Import')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorMessage
            return
        file = data["csv_file"].data
        output = self.process_csv(file)
        if output['number'] is not None:
            new_count = unicode(output['number'])
            IStatusMessage(self.request).addStatusMessage(
                "{} participants imported".format(new_count), 
                "info")
            if output['number'] < 1:
                IStatusMessage(self.request).addStatusMessage(
                "no participants imported. {}".format(errors), 
                "info")
            redirect_url = "{}/@@conference-attendee-importer".format(self.context.absolute_url())
            self.request.response.redirect(redirect_url)

    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
            "Hello No One",
            'info')
        redirect_url = "%s/" % self.context.absolute_url()
        self.request.response.redirect(redirect_url)

ConferenceAttendeeImporterView = wrap_form(ConferenceAttendeeImporterForm)