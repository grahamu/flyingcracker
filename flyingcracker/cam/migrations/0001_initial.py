# -*- coding: utf-8 -*-
import localflavor.us.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cam",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("url", models.URLField()),
                ("description", models.TextField(blank=True)),
                (
                    "state",
                    localflavor.us.models.USStateField(
                        default=b"CO",
                        max_length=2,
                        choices=[
                            (b"AL", b"Alabama"),
                            (b"AK", b"Alaska"),
                            (b"AS", b"American Samoa"),
                            (b"AZ", b"Arizona"),
                            (b"AR", b"Arkansas"),
                            (b"AA", b"Armed Forces Americas"),
                            (b"AE", b"Armed Forces Europe"),
                            (b"AP", b"Armed Forces Pacific"),
                            (b"CA", b"California"),
                            (b"CO", b"Colorado"),
                            (b"CT", b"Connecticut"),
                            (b"DE", b"Delaware"),
                            (b"DC", b"District of Columbia"),
                            (b"FL", b"Florida"),
                            (b"GA", b"Georgia"),
                            (b"GU", b"Guam"),
                            (b"HI", b"Hawaii"),
                            (b"ID", b"Idaho"),
                            (b"IL", b"Illinois"),
                            (b"IN", b"Indiana"),
                            (b"IA", b"Iowa"),
                            (b"KS", b"Kansas"),
                            (b"KY", b"Kentucky"),
                            (b"LA", b"Louisiana"),
                            (b"ME", b"Maine"),
                            (b"MD", b"Maryland"),
                            (b"MA", b"Massachusetts"),
                            (b"MI", b"Michigan"),
                            (b"MN", b"Minnesota"),
                            (b"MS", b"Mississippi"),
                            (b"MO", b"Missouri"),
                            (b"MT", b"Montana"),
                            (b"NE", b"Nebraska"),
                            (b"NV", b"Nevada"),
                            (b"NH", b"New Hampshire"),
                            (b"NJ", b"New Jersey"),
                            (b"NM", b"New Mexico"),
                            (b"NY", b"New York"),
                            (b"NC", b"North Carolina"),
                            (b"ND", b"North Dakota"),
                            (b"MP", b"Northern Mariana Islands"),
                            (b"OH", b"Ohio"),
                            (b"OK", b"Oklahoma"),
                            (b"OR", b"Oregon"),
                            (b"PA", b"Pennsylvania"),
                            (b"PR", b"Puerto Rico"),
                            (b"RI", b"Rhode Island"),
                            (b"SC", b"South Carolina"),
                            (b"SD", b"South Dakota"),
                            (b"TN", b"Tennessee"),
                            (b"TX", b"Texas"),
                            (b"UT", b"Utah"),
                            (b"VT", b"Vermont"),
                            (b"VI", b"Virgin Islands"),
                            (b"VA", b"Virginia"),
                            (b"WA", b"Washington"),
                            (b"WV", b"West Virginia"),
                            (b"WI", b"Wisconsin"),
                            (b"WY", b"Wyoming"),
                        ],
                    ),
                ),
            ],
            options={
                "ordering": ["title", "url"],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("title", models.CharField(max_length=30)),
            ],
            options={
                "ordering": ["title"],
                "verbose_name_plural": "categories",
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="cam",
            name="category",
            field=models.ForeignKey(to="cam.Category", on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
