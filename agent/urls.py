from django.urls import path
from . import views
from django.conf import settings  
from django.conf.urls.static import static 

app_name = 'agent'  
urlpatterns = [
    # index
    path('agents/dashboard',views.index,name='index'),
    # authentication
    path('agents/register', views.registerPage),
	  path('agents/', views.auth_view),
    path('agents/login', views.auth_view),   
	  path('agents/logout', views.logoutUser),
    # user-management       
    path('agents/users',views.users),
    path('agents/user-insert',views.user_insert),
    path('agents/user-add',views.user_add),
    path('agents/user-edit/<int:id>',views.user_edit),
    path('agents/user-update/<int:id>',views.user_update),
    path('agents/user-delete/<int:id>',views.user_delete),
    path('agents/user-profile',views.user_profile),
    path('agents/userprofile-add',views.user_profile_add),
    path('agents/user-profile-edit/<int:id>',views.user_profile_edit),
    path('agents/user-profile-update/<int:id>',views.user_profile_update),
    path('agents/user-profile-delete/<int:id>',views.user_profile_delete),
    path('agents/user-indivisual-profile/<int:id>',views.user_indivisual_profile),
  
    # channels  
    path('agents/channel-add',views.channel_add),  
    path('agents/channel-insert',views.channel_insert), 
    path('agents/channels',views.channels),  
    path('agents/channel-edit/<int:id>', views.channel_edit),  
    path('agents/channel-update/<int:id>', views.channel_update),  
    path('agents/channel-delete/<int:id>', views.channel_destroy),  

  # amenities
    path('agents/amenities-insert',views.amenities_insert),  
    path('agents/amenities-add',views.amenities_add), 
    path('agents/amenities',views.amenities),  
    path('agents/amenities-edit/<int:id>', views.amenities_edit),  
    path('agents/amenities-update/<int:id>', views.amenities_update),  
    path('agents/amenities-delete/<int:id>', views.amenities_destroy),
    
    # activity
    path('agents/activity',views.activity),  
    path('agents/activity-add',views.activity_add),
    path('agents/activity-insert',views.activity_insert),  
    path('agents/activity-edit/<int:id>', views.activity_edit),  
    path('agents/activity-update/<int:id>', views.activity_update),  
    path('agents/activity-delete/<int:id>', views.activity_destroy),
    # rentals
    path('agents/rental-add',views.rental_add),
    path('agents/rental-insert',views.rental_insert),
    path('agents/rentals',views.rentals),  
    path('agents/rental-edit/<int:id>', views.rental_edit),  
    path('agents/rental-update/<int:id>', views.rental_update),  
    path('agents/rental-delete/<int:id>', views.rental_destroy),

    # rental-type  
    path('agents/rental-type-add',views.rental_type_add),  
    path('agents/rental-type-insert',views.rental_type_insert), 
    path('agents/rental-type',views.rental_type),  
    path('agents/rental-type-edit/<int:id>', views.rental_type_edit),  
    path('agents/rental-type-update/<int:id>', views.rental_type_update),  
    path('agents/rental-type-delete/<int:id>', views.rental_type_destroy), 
    # tax
    path('agents/tax-add',views.tax_add), 
    path('agents/tax-insert',views.tax_insert), 
    path('agents/tax',views.tax),  
    path('agents/tax-edit/<int:id>', views.tax_edit),  
    path('agents/tax-update/<int:id>', views.tax_update),  
    path('agents/tax-delete/<int:id>', views.tax_destroy), 
    # tax-Type
    path('agents/tax-type', views.tax_type),
    path('agents/tax-type-add', views.tax_type_add),
    path('agents/tax-type-insert', views.tax_type_insert),
    path('agents/tax-type-edit/<int:id>', views.tax_type_edit), 
    path('agents/tax-type-update/<int:id>', views.tax_type_update),  
    path('agents/tax-type-delete/<int:id>', views.tax_type_destroy), 
    # Policy
    path('agents/policy', views.policy),
    path('agents/policy-add', views.policy_add),
    path('agents/policy-insert', views.policy_insert),
    path('agents/policy-edit/<int:id>', views.policy_edit), 
    path('agents/policy-update/<int:id>', views.policy_update),
    path('agents/policy-delete/<int:id>', views.policy_destroy), 
    # rate-Type 
    path('agents/rate-type', views.rate_type),
    path('agents/rate-type-add', views.rate_type_add),
    path('agents/rate-type-insert', views.rate_type_insert),
    path('agents/rate-type-edit/<int:id>', views.rate_type_edit), 
    path('agents/rate-type-update/<int:id>', views.rate_type_update),  
    path('agents/rate-type-delete/<int:id>', views.rate_type_destroy), 

    # rate 
    path('agents/rate', views.rate),
    path('agents/rate-add', views.rate_add),
    path('agents/rate-insert', views.rate_insert),
    path('agents/rate-edit/<int:id>', views.rate_edit), 
    path('agents/rate-update/<int:id>', views.rate_update),  
    path('agents/rate-delete/<int:id>', views.rate_destroy), 
      # booking
    path('agents/bookings',views.booking),
    path('agents/booking-view/<int:id>',views.booking_view),
    path('agents/booking-edit/<int:id>',views.booking_edit),
    path('agents/booking-update/<int:id>',views.booking_update),

     # rate-Type 
    path('agents/discount-type', views.discount_type),
    path('agents/discount-type-add', views.discount_type_add),
    path('agents/discount-type-insert', views.discount_type_insert),
    path('agents/discount-type-edit/<int:id>', views.discount_type_edit), 
    path('agents/discount-type-update/<int:id>', views.discount_type_update),  
    path('agents/discount-type-delete/<int:id>', views.discount_type_destroy),

    # discount
    path('agents/discounts', views.discount),
    path('agents/discount-add', views.discount_add),
    path('agents/discount-insert', views.discount_insert),
    path('agents/discount-edit/<int:id>', views.discount_edit), 
    path('agents/discount-update/<int:id>', views.discount_update),  
    path('agents/discount-delete/<int:id>', views.discount_destroy), 

     #invoice   
    path('agents/invoice/', views.InvoiceListView.as_view(), name="invoice-list"),
    path('agents/invoice-create/', views.createInvoice, name="invoice-create"),
    path('agents/invoice-detail/<id>', views.view_PDF, name='invoice-detail'),
    path('agents/invoice-download/<id>', views.generate_PDF, name='invoice-download'),
    path('agents/company-add',views.company_add), 
    path('agents/company-insert',views.company_insert), 
    path('agents/company',views.company),  
    path('agents/company-edit/<int:id>', views.company_edit),  
    path('agents/company-update/<int:id>', views.company_update),  
    path('agents/company-delete/<int:id>', views.company_destroy),
     # attributes
    path('agents/attributes-insert',views.attributes_insert),  
    path('agents/attributes-add',views.attributes_add), 
    path('agents/attributes',views.attributes),  
    path('agents/attributes-edit/<int:id>', views.attributes_edit),  
    path('agents/attributes-update/<int:id>', views.attributes_update),  
    path('agents/attributes-delete/<int:id>', views.attributes_destroy),

    path('agents/calendar', views.calendar),
    path('agents/reports', views.reports),
    # Partner category  
    path('agents/partner-category-add',views.category_add),  
    path('agents/partner-category-insert',views.category_insert), 
    path('agents/partners-category',views.category),  
    path('agents/partner-category-edit/<int:id>', views.category_edit),  
    path('agents/partner-category-update/<int:id>', views.category_update),  
    path('agents/partner-category-delete/<int:id>', views.category_destroy),

# Partner 
    path('agents/partner-add',views.partner_add),  
    path('agents/partner-insert',views.partner_insert), 
    path('agents/partner',views.partner),  
    path('agents/partner-edit/<int:id>', views.partner_edit),  
    path('agents/partner-update/<int:id>', views.partner_update),  
    path('agents/partner-delete/<int:id>', views.partner_destroy),


  
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)   