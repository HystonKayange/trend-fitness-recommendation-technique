from formtools.wizard.views import SessionWizardView
from .forms import ProfileFormSection1, ProfileFormSection2
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from .models import Profile


FORMS = [("section1", ProfileFormSection1), ("section2", ProfileFormSection2),]

TEMPLATES = {
        '0': 'account/profile_form1.html',
        '1': 'account/profile_form2.html',
    }


class MyWizard(SessionWizardView):
    # Define form_list to specify the order of the forms
    form_list = [ProfileFormSection1, ProfileFormSection2]

    # Optionally define templates for each step
    def get_template_names(self):
        return TEMPLATES[self.steps.current]

    def done(self, form_list, form_dict, **kwargs):
        user = self.request.user

        # Check if all forms are valid
        if all(form.is_valid() for form in form_dict.values()):
            # Check if an instance already exists for the user
            instance, created = Profile.objects.get_or_create(user=user)

            # Iterate over the form list and save the data to the same instance
            for form_key, form in form_dict.items():
                form.instance = instance  # Assign the existing instance to the form
                form.save(commit=False)

                # Iterate over the cleaned data of the form and set it on the instance
                for field, value in form.cleaned_data.items():
                    setattr(instance, field, value)

            # After all forms are processed, save the instance
            instance.save()

            # Perform additional actions
            print("All forms are valid. Data saved successfully.")
            return redirect("/")
        else:
            # At least one form is invalid, return to the previous step
            return self.render_revalidation_failure(form_list, form_dict, **kwargs)



    def render_revalidation_failure(self, form_list, form_dict, **kwargs):
        # Find the first invalid form
        for form_key, form in form_dict.items():
            if not form.is_valid():
                # Get the step associated with the invalid form
                step_index = self.get_form_step_data(form_key)['step']

                # Redirect back to the step with the invalid form
                return HttpResponseRedirect(self.get_step_url(step_index))

        # If no invalid form is found, redirect to the first step
        return HttpResponseRedirect(self.get_step_url(0))
