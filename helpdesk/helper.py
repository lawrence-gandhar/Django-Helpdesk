#
# Author : Lawrence Gandhar
# July - 2019
# This script will generate the data for the graphs displayed on dashboard  
# 


import calendar, re
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q
from helpdesk.models import Ticket

"""
Output
=============================================================================================
[
	['x', '2010-01-01', '2011-01-01', '2012-01-01', '2013-01-01', '2014-01-01', '2015-01-01'],
	['Taken By Me', 30, 200, 100, 400, 150, 250],
	['Open tickets', 50, 20, 10, 40, 15, 25]
]
"""

#===============================================================================================
# time series generation for line charts
#===============================================================================================

def default_series(series_data,year=True):
	if year:
		for key in series_data.keys():
			for i in range(1,13):
				if key == "x_axis":
					series_data[key].append(calendar.month_abbr[i])
				else:
					series_data[key].append(0)
	else:	
		for key in series_data.keys():							
			for i in range(1,32):
				if key == "x_axis":
					series_data[key].append(i)
				else:
					series_data[key].append(0)
		
	return series_data


#===============================================================================================
# Year Wise Data Series Generation
#===============================================================================================

def year_wise_data(request, status_codes, series_data, tickets):
	for ticket in tickets:
		series_data[status_codes[ticket["status"]]][ticket["created"].month] += 1	
		
		if ticket["assigned_to"] == request.user.id:
			series_data["assigned_tickets"][ticket["created"].month] += 1

		if ticket["assigned_to"] is None:
			series_data["unassigned_tickets"][ticket["created"].month] += 1	
	return series_data
	


#===============================================================================================
# Year Wise Data Series Generation
#===============================================================================================

def month_wise_data(request, status_codes, series_data, tickets):
	for ticket in tickets:
	    print(ticket["created"].day)
	    series_data[status_codes[ticket["status"]]][ticket["created"].day] += 1	
	    
	    if ticket["assigned_to"] == request.user.id:
	        series_data["assigned_tickets"][ticket["created"].day] += 1
	    if ticket["assigned_to"] is None:
	        series_data["unassigned_tickets"][ticket["created"].day] += 1	
	return series_data


#===============================================================================================
# Line Chart Data generation based on year, month, or both
#
# If Year then will create timeseries for all months
# If month then will create timeseries data for the respective number of days present 
# If year is None and month is not then current year will be selected by default
#===============================================================================================

def line_chart_data(request, s_year = None, s_month = None):

	status_codes = dict({
		1: "open_tickets", 
		2: "reopened_tickets",
		3: "resolved_tickets",		
		4: "closed_tickets", 
		5: "duplicate_tickets",
		6: "onhold_tickets",		
	})		

	series_data = dict({
						"x_axis" : ["x"],
						"open_tickets" : ["Open Tickets"], 
						"closed_tickets" : ["Closed Tickets"], 
						"reopened_tickets" : ["Reopened Tickets"],
						"resolved_tickets" : ["Resolved Tickets"],
						"duplicate_tickets" : ["Duplicate Tickets"],
						"onhold_tickets" : ["OnHold Tickets"], 
						"assigned_tickets" : ["Tickets Assigned To Me"], 
						"unassigned_tickets" : ["Unassigned Tickets"],
					})
		
	if s_year is not None:
	    if s_month is not None:
	        default_series(series_data, False)
	        tickets = Ticket.objects.filter(created__year = s_year, created__month = str(int(s_month) + 1))
	        tickets = tickets.values('status', 'created', 'assigned_to')
	        month_wise_data(request, status_codes, series_data, tickets)
	    else:
		    # for year
		    default_series(series_data, True)
		    tickets = Ticket.objects.filter(created__year = s_year).values('status', 'created', 'assigned_to')
		    year_wise_data(request, status_codes, series_data, tickets)
		    
	else:
	    s_year = timezone.now().year
	    
	    if s_month is not None:
	        default_series(series_data, False)
	        tickets = Ticket.objects.filter(created__year = s_year, created__month = str(int(s_month) + 1))
	        tickets = tickets.values('status', 'created', 'assigned_to')
	        month_wise_data(request, status_codes, series_data, tickets)
	    else:
	        default_series(series_data, True)
	        tickets = Ticket.objects.filter(created__year = s_year).values('status', 'created', 'assigned_to')
	        year_wise_data(request, status_codes, series_data, tickets)
		
			
	main_data_series = []
	for item in series_data.keys():
		main_data_series.append(series_data[item])

	return main_data_series


#===============================================================================================
# Pie Chart Data generation based on year, month
#===============================================================================================

def month_pie_series(request, s_year, s_month):
    year_month_series_data = [ 
        ["Open Tickets", Ticket.objects.filter(status = Ticket.OPEN_STATUS, created__year = s_year, created__month = str(int(s_month) + 1)).count()], 
        ["Closed Tickets", Ticket.objects.filter(status = Ticket.CLOSED_STATUS, created__year = s_year, created__month = str(int(s_month) + 1)).count()],
        ["Reopened Tickets", Ticket.objects.filter(status = Ticket.REOPENED_STATUS, created__year = s_year, created__month = str(int(s_month) + 1)).count()],
        ["Resolved Tickets", Ticket.objects.filter(status = Ticket.RESOLVED_STATUS, created__year = s_year, created__month = str(int(s_month) + 1)).count()],
        ["Duplicate Tickets", Ticket.objects.filter(status = Ticket.DUPLICATE_STATUS, created__year = s_year, created__month = str(int(s_month) + 1)).count()],
        ["OnHold Tickets", Ticket.objects.filter(status = Ticket.ONHOLD_STATUS, created__year = s_year, created__month = str(int(s_month) + 1)).count()],
        ["Tickets Assigned To Me", Ticket.objects.filter(assigned_to=request.user, created__year = s_year, created__month = str(int(s_month) + 1)).count()],
        ["Unassigned Tickets", Ticket.objects.filter(assigned_to__isnull=True, created__year = s_year, created__month = str(int(s_month) + 1)).count()],
    ]
    
    return year_month_series_data

#===============================================================================================
# Pie Chart Data generation based on year
#===============================================================================================

def year_pie_series(request, s_year, s_month):
    year_series_data = [ 
        ["Open Tickets", Ticket.objects.filter(status = Ticket.OPEN_STATUS, created__year = s_year).count()], 
        ["Closed Tickets", Ticket.objects.filter(status = Ticket.CLOSED_STATUS, created__year = s_year).count()],
        ["Reopened Tickets", Ticket.objects.filter(status = Ticket.REOPENED_STATUS, created__year = s_year).count()],
        ["Resolved Tickets", Ticket.objects.filter(status = Ticket.RESOLVED_STATUS, created__year = s_year).count()],
        ["Duplicate Tickets", Ticket.objects.filter(status = Ticket.DUPLICATE_STATUS, created__year = s_year).count()],
        ["OnHold Tickets", Ticket.objects.filter(status = Ticket.ONHOLD_STATUS, created__year = s_year).count()],
        ["Tickets Assigned To Me", Ticket.objects.filter(assigned_to=request.user, created__year = s_year).count()],
        ["Unassigned Tickets", Ticket.objects.filter(assigned_to__isnull=True, created__year = s_year).count()],
    ]
    return year_series_data



#===============================================================================================
# Pie Chart Data generation based on year, month, or both
#
# If Year then will create timeseries for all months
# If month then will create timeseries data for the respective number of days present 
# If year is None and month is not then current year will be selected by default
#===============================================================================================

def pie_chart_data(request, s_year = None, s_month = None):
    if s_year is not None:
        if s_month is not None:
            return month_pie_series(request, s_year, s_month)
        else:
            return year_pie_series(request, s_year, s_month)
    else:
        s_year = timezone.now().year
        
        if s_month is not None:
            return month_pie_series(request, s_year, s_month)
        else:
            return year_pie_series(request, s_year, s_month)



#===============================================================================================
# Ticket details assigned to Users
#
#===============================================================================================

def tickets_assigned_to_users():
	from django.db import connection
	
	with connection.cursor() as cursor:
		cursor.execute(
			'''select AU.id, AU.first_name, AU.last_name, AU.is_active, AU.email, AU.is_superuser,
				(select count(id) from helpdesk_ticket where assigned_to_id = AU.id) as assigned_tickets,
				(select count(id) from helpdesk_ticket where status = 1 and assigned_to_id = AU.id) as open_tickets,
				(select count(id) from helpdesk_ticket where status = 2 and assigned_to_id = AU.id) as reopen_tickets,
				(select count(id) from helpdesk_ticket where status = 3 and assigned_to_id = AU.id) as resolved_tickets,
				(select count(id) from helpdesk_ticket where status = 4 and assigned_to_id = AU.id) as closed_tickets,
				(select count(id) from helpdesk_ticket where status = 5 and assigned_to_id = AU.id) as duplicate_tickets,
				(select count(id) from helpdesk_ticket where status = 6 and assigned_to_id = AU.id) as onhold_tickets
				from auth_user AU  
				where AU.id in (select id from auth_user) order by id asc''')
		columns = [col[0] for col in cursor.description]
		return [dict(zip(columns, row)) for row in cursor.fetchall()]

            

	








