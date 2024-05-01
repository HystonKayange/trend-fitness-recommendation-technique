from django import forms
from .models import BlogPost, Category, Comment
from ckeditor.widgets import CKEditorWidget


class CreateBlogPostForm(forms.ModelForm):

    category = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input container'}), 
        queryset=Category.objects.all().exclude(id=1),
    )

    class Meta:
        model = BlogPost
        fields = ['category', 'title', 'body', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control ', 'required':'required',  'autofocus': 'True'}),
            'body': forms.CharField(widget=CKEditorWidget()),
            'image': forms.FileInput(attrs={'class': 'form-control', 'onchange': 'readURL(this)', 'id':'id_image_file'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
        }


    def clean(self):
        super(CreateBlogPostForm, self).clean()

        title = self.cleaned_data.get('title')
        category = self.cleaned_data.get('category')
        body = self.cleaned_data.get('body')

        if len(title) > 250:
            self.errors['title'] = self.error_class(['A maximum of 250 characters is required in this field'])
        elif len(title) < 5:
            self.errors['title'] = self.error_class(['A mininmum of 5 characters is required in this field'])

        if len(body) < 250:
            self.errors['body'] = self.error_class(['A mininmum of 250 words is required in this field'])
       
        if not category:
            self.errors['category'] = self.error_class(['Atleast one category must be selected is required in this field'])

        return self.cleaned_data


class EditBlogPostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image', 'category']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control ', 'required':'required',  'autofocus': 'True'}),
            'category': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input' }),
            'body': forms.CharField(widget=CKEditorWidget()),
            'image': forms.FileInput(attrs={'class': 'form-control', 'onchange': 'readURL(this)', 'id':'id_image_file'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }


    def save(self, commit=True):
        blog_post = self.instance
        blog_post.title = self.cleaned_data['title']
        blog_post.body = self.cleaned_data['body']
        for i in self.cleaned_data['category']:
            blog_post.category.set(self.cleaned_data['category'])

        if self.cleaned_data['image']:
            blog_post.image = self.cleaned_data['image']

        if len(self.cleaned_data['title']) < 4:
            self.errors['title'] = self.error_class(['Atleast one category must be selected is required in this field'])

        if commit:
            blog_post.save()
        return blog_post
