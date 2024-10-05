document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    if (!calendarEl) {
        console.error("Calendar container not found!");
        return;
    }

    var events = repaymentDates.map(item => ({
        title: `$${item.amount}`,
        start: item.date,               
        allDay: true,              
        color: 'red',              
    }));

    // Initialize the FullCalendar
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: events 
    });

    calendar.render(); 
});
