from abc import ABC, abstractmethod
from django.db.models import ForeignKey, ManyToManyField
from timeline.models import TimelineEntry
from timeline.models.integrate.entry import TLEntry


class BaseEntry(ABC):
    """
    Base entry class for generating timeline entries
    """
    def __init__(self, model):
        self.model = model

        # if model differences() method is called
        # results will be stored here.
        self.changes = None

    @abstractmethod
    def have_changes(self):
        """
        Abstract method for determining if there are any
        changes to the module

        Arguments:
            void

        Return:
            bool    True if changes are present. False if not.
        """
        pass

    @abstractmethod
    def content(self):
        """
        Abstract method to get the markdown content

        Arguments:
            void


        Return:
            string      The markdown for entry content.
        """
        pass

    @abstractmethod
    def sum_changes(self):
        """
        Provides a small summary of changes

        Arguments:
            void

        Returns:
            string      The summary of changes.
        """
        pass

    def create_entry(self, **kwargs):
        """
        Creates the timeline entry model.

        Arguments:
            Expected kwargs:
                - parent            The parent entry
                - entry_type        Type of timeline entry
                - status            Workflow status, i.e Draft.
                - requested_by      Uer that causes the entry to be created.

            In all cases, if not provided, then defaults will be
            applied and changes can still be processed.

        Returns:
            TimelineEntry object    The entry that was created.
        """
        parent = kwargs.get('parent', None)
        entry_type = kwargs.get('entry_type', 'Generic')
        status = kwargs.get('status', 'Draft')
        requested_by = kwargs.get('requested_by', None)

        # if there are not changes, then prevents an
        # entry being made
        if not self.have_changes():
            return None

        # create the timeline entry
        title = self.model.title()
        changes = self.content()
        module_code = self.get_module_code()
        object_id = self.model.pk
        content_object = self.model

        return TimelineEntry.objects.create(
            title=title,
            changes=changes,
            module_code=module_code,
            object_id=object_id,
            content_object=content_object,
            parent_entry=parent,
            entry_type=entry_type,
            status=status,
            changes_by=requested_by
        )

    def get_module_code(self):
        """
        Gets the module code from the model
        """
        cls = self.model.__class__

        # if it is not a sublcass of TLEntry, then we know
        # that the model is Module, so return its
        # module code attribute.
        if not issubclass(cls, TLEntry):
            return self.model.module_code
        return self.model.module_code()

    def title(self):
        """
        Gets the title for the timeline entry
        """
        return self.model.title()


class InitEntry(BaseEntry):
    """
    Creates timeline entries of models that have just been created.
    """
    def __init__(self, model):
        super(InitEntry, self).__init__(model)

    def have_changes(self):
        """
        Method to get any changes from entry.
        """
        # since this is a new model, will have changes regardless.
        return True

    def content(self):
        """
        Method to get the markdown content

        Arguments:
            void


        Return:
            string      The markdown for entry content.
        """

        # get the changes
        diff = self.model.differences()

        md = ""
        # loop through each field and generate
        # the markup for each field
        for field, changes in diff.items():
            field_str = field.replace("_", " ")
            updated = changes[1]

            # get field object from model
            field_type = self.model._meta.get_field(field)

            # if a ForeignKey object, get the stored
            # object and swap the value to display usable data
            # as oppossed to a id.
            if isinstance(field_type, ForeignKey):
                key_object = field_type.rel.to
                updated = key_object.objects.get(pk=updated)

            # if a ManyToManyField, ignore as django
            # makes it impossible to tell if there are any
            # changes with this object.
            if isinstance(field_type, ManyToManyField):
                continue

            md += "* {}: {}\n".format(field_str, updated)
        return md

    def sum_changes(self):
        """
        Provides a small summary of changes

        Arguments:
            void

        Returns:
            string      The summary of changes.
        """
        return "{} has been created for {}".format(
            self.model.title(),
            self.get_module_code()
        )


class UpdateEntry(BaseEntry):
    def __init__(self, model):
        super(UpdateEntry, self).__init__(model)

    def get_differences(self):
        if self.changes is None:
            self.changes = self.model.differences()
        return self.changes

    def have_changes(self):
        """
        Method to get any changes from entry.
        """
        return bool(self.get_differences())

    def content(self):
        """
        Method to get the markdown content

        Arguments:
            void


        Return:
            string      The markdown for entry content.
        """

        diff = self.model.differences()
        md = ""

        # loop through each field, then generate
        # the markdown for showing original and updated fields
        for field, changes in diff.items():
            field_str = field.replace("_", " ")
            original = changes[0]
            updated = changes[1]

            field_type = self.model._meta.get_field(field)

            # if a ForeignKey object, get the stored
            # object and swap the value to display usable data
            # as oppossed to a id.
            if isinstance(field_type, ForeignKey):
                key_object = field_type.rel.to
                original = key_object.objects.get(pk=original)
                updated = key_object.objects.get(pk=updated)

            # if a ManyToManyField, ignore as django
            # makes it impossible to tell if there are any
            # changes with this object.
            if isinstance(field_type, ManyToManyField):
                continue

            md += "* {}: {} -> {}\n".format(field_str, original, updated)
        return md

    def sum_changes(self):
        """
        Provides a small summary of changes

        Arguments:
            void

        Returns:
            string      The summary of changes.
        """
        n_changes = len(self.get_differences())
        return "There are {} changes to {}".format(
            n_changes, self.model.title()
        )