document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    if (!calendarEl) {
        console.error("Calendar container not found!");
        return;
    }

    var events = repaymentDates.map(date => ({
        start: date,               
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
