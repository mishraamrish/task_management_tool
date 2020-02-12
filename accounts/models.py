from django.core.validators import URLValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class EmployeeManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Profile(models.Model):
    class Meta:
        db_table = "profile"

    name = models.CharField(blank=False, null=False, max_length=56)
    title = models.CharField(blank=False, null=False, max_length=56)


class Company(models.Model):
    class Meta:
        db_table = "company"

    name = models.CharField(blank=False, null=False, max_length=56)
    spoc_name = models.CharField(blank=False, null=False, max_length=56)
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    phone_number = models.CharField(blank=True, null=True, max_length=20)
    is_active = models.BooleanField(default=True)


class Address(models.Model):
    address_type = 'company_address'
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
    )
    name = models.CharField(
        "Full name",
        max_length=1024,
    )

    address1 = models.CharField(
        "Address line 1",
        max_length=1024,
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024,
    )

    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )

    city = models.CharField(
        "City",
        max_length=1024,
    )

    country = models.CharField(
        "Country",
        max_length=28,
    )

    class Meta:
        db_table = "address"
        verbose_name = "Address"
        verbose_name_plural = "Addresses"


class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="departments")
    name = models.CharField(max_length=128, blank=False)

    class Meta:
        unique_together = ("company", "name")
        db_table = "department"


class Employee(AbstractUser):
    class Meta:
        db_table = "employee"
    username = None
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = EmployeeManager()
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="employees")
    dob = models.DateField(verbose_name="Date of Birth", blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="employees_profile")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="employees_company")
    phone_number = models.CharField(blank=True, null=True, max_length=20)
    alternate_email = models.EmailField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="employee_departments")
    bio = models.CharField(blank=True, null=True, max_length=500)
    profilePicture = models.TextField(validators=[URLValidator()])

