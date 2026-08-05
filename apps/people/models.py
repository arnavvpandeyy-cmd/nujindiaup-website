"""
apps/people/models.py

Models for:
- OfficeBearer: UP-level office bearers (President, Sec. General, VPs, etc.)
- StateUnit: City chapter of NUJ Uttar Pradesh
- StateUnitMember: Office bearers within each city unit
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from apps.core.models import TimestampedModel


# ─────────────────────────────────────────────
# All 75 Districts of Uttar Pradesh
# ─────────────────────────────────────────────
INDIAN_STATES = [
    ('AGR', 'Agra'),
    ('ALG', 'Aligarh'),
    ('AMB', 'Ambedkar Nagar'),
    ('AMT', 'Amethi'),
    ('AMR', 'Amroha'),
    ('AYD', 'Ayodhya (Faizabad)'),
    ('AZG', 'Azamgarh'),
    ('BDN', 'Badaun'),
    ('BGP', 'Bagpat'),
    ('BAH', 'Bahraich'),
    ('BLI', 'Ballia'),
    ('BRM', 'Balrampur'),
    ('BND', 'Banda'),
    ('BAR', 'Barabanki'),
    ('BRL', 'Bareilly'),
    ('BST', 'Basti'),
    ('BIJ', 'Bijnor'),
    ('BRN', 'Bulandshahr'),
    ('CND', 'Chandauli'),
    ('CHT', 'Chitrakoot'),
    ('DDB', 'Deoria'),
    ('ETH', 'Etah'),
    ('ETW', 'Etawah'),
    ('FAR', 'Farrukhabad'),
    ('FTP', 'Fatehpur'),
    ('FZB', 'Firozabad'),
    ('GBN', 'Gautam Buddha Nagar (Noida)'),
    ('GZB', 'Ghaziabad'),
    ('GPR', 'Ghazipur'),
    ('GND', 'Gonda'),
    ('GKP', 'Gorakhpur'),
    ('HMR', 'Hamirpur'),
    ('HAP', 'Hapur'),
    ('HRD', 'Hardoi'),
    ('HTP', 'Hathras'),
    ('JAL', 'Jalaun'),
    ('JPR', 'Jaunpur'),
    ('JHS', 'Jhansi'),
    ('KNN', 'Kannauj'),
    ('KNP', 'Kanpur Nagar'),
    ('KDH', 'Kanpur Dehat'),
    ('KSG', 'Kasganj'),
    ('KSH', 'Kaushambi'),
    ('KHR', 'Kheri (Lakhimpur)'),
    ('KSN', 'Kushinagar'),
    ('LLT', 'Lalitpur'),
    ('LKO', 'Lucknow'),
    ('MHB', 'Maharajganj'),
    ('MHP', 'Mahoba'),
    ('MNP', 'Mainpuri'),
    ('MTH', 'Mathura'),
    ('MAU', 'Mau'),
    ('MRT', 'Meerut'),
    ('MDR', 'Mirzapur'),
    ('MRD', 'Moradabad'),
    ('MZN', 'Muzaffarnagar'),
    ('PBH', 'Pilibhit'),
    ('PTN', 'Pratapgarh'),
    ('PRY', 'Prayagraj (Allahabad)'),
    ('RBR', 'Raebareli'),
    ('RAM', 'Rampur'),
    ('SHJ', 'Saharanpur'),
    ('SMB', 'Sambhal'),
    ('SKN', 'Sant Kabir Nagar'),
    ('BHD', 'Sant Ravidas Nagar'),
    ('SHP', 'Shahjahanpur'),
    ('SHM', 'Shamli'),
    ('SRV', 'Shravasti'),
    ('SDH', 'Siddharthnagar'),
    ('STP', 'Sitapur'),
    ('SNB', 'Sonbhadra'),
    ('STG', 'Sultanpur'),
    ('UNO', 'Unnao'),
    ('VAR', 'Varanasi'),
]



class OfficeBearer(TimestampedModel):
    """
    UP-level office bearer of NUJ Uttar Pradesh.
    """
    CATEGORY_CHOICES = [
        ('president', 'President'),
        ('working_president', 'Working President'),
        ('secretary_general', 'Secretary General'),
        ('treasurer', 'Treasurer'),
        ('vice_president', 'Vice President'),
        ('joint_secretary', 'Joint Secretary'),
        ('executive_member', 'Executive Member'),
        ('zonal_coordinator', 'Zonal Coordinator'),
        ('patron', 'Patron'),
        ('advisor', 'Advisor'),
    ]

    name = models.CharField(max_length=200, verbose_name=_("Full Name"))
    slug = models.SlugField(max_length=220, unique=True, blank=True, verbose_name=_("Slug"))
    role = models.CharField(max_length=200, verbose_name=_("Role / Designation"))
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='executive_member',
        verbose_name=_("Category")
    )
    state = models.CharField(
        max_length=3,
        choices=INDIAN_STATES,
        blank=True,
        verbose_name=_("City")
    )
    zone = models.CharField(max_length=100, blank=True, verbose_name=_("Zone"))
    bio = models.TextField(blank=True, verbose_name=_("Bio"))
    photo = models.ImageField(upload_to='bearers/', blank=True, null=True, verbose_name=_("Photo"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone"))
    show_contact = models.BooleanField(
        default=False,
        verbose_name=_("Show Contact Publicly"),
        help_text=_("If checked, email/phone will be visible to public.")
    )
    term_start = models.DateField(blank=True, null=True, verbose_name=_("Term Start"))
    term_end = models.DateField(blank=True, null=True, verbose_name=_("Term End"))
    is_featured = models.BooleanField(default=False, verbose_name=_("Featured on Homepage"))
    is_national = models.BooleanField(default=False, verbose_name=_("National Office Bearer"), help_text=_("Mark this person as a national-level office bearer for homepage display."))
    is_published = models.BooleanField(default=True, verbose_name=_("Published"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))

    class Meta:
        verbose_name = _("Office Bearer")
        verbose_name_plural = _("Office Bearers")
        ordering = ['order', 'category', 'name']

    def __str__(self):
        return f"{self.name} — {self.role}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_state_display_name(self):
        return dict(INDIAN_STATES).get(self.state, self.state)


class StateUnit(TimestampedModel):
    """
    City-level chapter of NUJ Uttar Pradesh.
    """
    name = models.CharField(max_length=200, verbose_name=_("Unit Name"))
    slug = models.SlugField(max_length=220, unique=True, blank=True, verbose_name=_("Slug"))
    state = models.CharField(
        max_length=3,
        choices=INDIAN_STATES,
        unique=True,
        verbose_name=_("City")
    )
    established_year = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("Established Year"))
    description = models.TextField(blank=True, verbose_name=_("About the Unit"))
    address = models.TextField(blank=True, verbose_name=_("Office Address"))
    phone = models.CharField(max_length=30, blank=True, verbose_name=_("Phone"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    website = models.URLField(blank=True, verbose_name=_("Website"))
    cover_image = models.ImageField(upload_to='city_units/', blank=True, null=True, verbose_name=_("Cover Image"))
    member_count = models.PositiveIntegerField(default=0, verbose_name=_("Member Count"))
    is_published = models.BooleanField(default=True, verbose_name=_("Published"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))

    class Meta:
        verbose_name = _("City Unit")
        verbose_name_plural = _("City Units")
        ordering = ['order', 'state']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_state_name(self):
        """Returns the city display name."""
        return dict(INDIAN_STATES).get(self.state, self.state)


class StateUnitMember(TimestampedModel):
    """
    Office bearer within a city unit.
    """
    state_unit = models.ForeignKey(
        StateUnit,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name=_("City Unit")
    )
    name = models.CharField(max_length=200, verbose_name=_("Full Name"))
    role = models.CharField(max_length=200, verbose_name=_("Role"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    photo = models.ImageField(upload_to='city_members/', blank=True, null=True, verbose_name=_("Photo"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Order"))

    class Meta:
        verbose_name = _("City Unit Member")
        verbose_name_plural = _("City Unit Members")
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.role}) — {self.state_unit.name}"
