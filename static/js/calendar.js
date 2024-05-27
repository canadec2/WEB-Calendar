$(document).ready(function() {
    var currentEvent;

    // Initialize the FullCalendar
    $('#calendar').fullCalendar({
        locale: 'ru',
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        editable: true,
        droppable: true,
        events: [],
        selectable: true,
        selectHelper: true,
        select: function(start, end) {
            $('#createEventModal').modal('show');
            $('#event-start').val(start.format('DD-MM-YYYY HH:mm'));
            $('#event-end').val(end.format('DD-MM-YYYY HH:mm'));
        },
        eventClick: function(event) {
            currentEvent = event;
            openEditModal(event);
        },
        eventDrop: function(event) {
            updateEventLists();
        },
        eventResize: function(event) {
            updateEventLists();
        },
        viewRender: function(view) {
            updateEventLists();
        },
        eventRender: function(event, element) {
            var startTime = moment(event.start).format('HH:mm');
            var endTime = moment(event.end).format('HH:mm');
            var eventTimeRange = startTime + '-' + endTime;
            element.find('.fc-time').remove(); // Удаляем стандартное время
            element.find('.fc-title').text(eventTimeRange + ' ' + event.title);
            element.css('background-color', event.color);
        },
        allDaySlot: false,
        minTime: '00:00:00',
        maxTime: '24:00:00',
        slotDuration: '00:30:00',
        slotLabelInterval: '01:00:00',
        contentHeight: 'auto',
        height: 'auto',
        nowIndicator: true,
        scrollTime: '00:00:00',
        aspectRatio: 1.8, // Adjust aspect ratio to allow for better vertical space usage
        handleWindowResize: true,
        defaultView: 'agendaWeek',
        scrollable: true,
        businessHours: {
            start: '00:00', // a start time (10am in this example)
            end: '24:00', // an end time (6pm in this example)
        },
    });

    // Initialize the datepicker
    $('#datepicker').datepicker({
        dateFormat: 'dd-mm-yy',
        dayNamesMin: ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"],
        monthNames: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", 
                     "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
        firstDay: 1,
        onSelect: function(dateText) {
            var date = $(this).datepicker('getDate');
            $('#calendar').fullCalendar('gotoDate', date);
        }
    });

    // Initialize the datetimepickers
    $('.datetimepicker').datetimepicker({
        format: 'd-m-Y H:i',
        step: 15,
        lang: 'ru'
    });

    // Handle create event form submission
    $('#createEventForm').on('submit', function(e) {
        e.preventDefault();
        var title = $('#event-title').val();
        var start = $('#event-start').val();
        var end = $('#event-end').val();
        var description = $('#event-description').val();
        var color = $('#event-color').val();
        var repeat = $('#event-repeat').val();

        if (title) {
            var eventData = {
                title: title,
                start: moment(start, 'DD-MM-YYYY HH:mm').format(),
                end: moment(end, 'DD-MM-YYYY HH:mm').format(),
                description: description,
                color: color,
                repeat: repeat
            };

            $('#calendar').fullCalendar('renderEvent', eventData, true);
            $('#createEventModal').modal('hide');
            $(this).trigger('reset');
            updateEventLists();
        } else {
            alert("Название не может быть пустым. Пожалуйста, заполните все обязательные поля.");
        }
    });

    // Handle edit event form submission
    $('#editEventForm').on('submit', function(e) {
        e.preventDefault();
        currentEvent.title = $('#edit-event-title').val();
        currentEvent.start = moment($('#edit-event-start').val(), 'DD-MM-YYYY HH:mm').format();
        currentEvent.end = moment($('#edit-event-end').val(), 'DD-MM-YYYY HH:mm').format();
        currentEvent.description = $('#edit-event-description').val();
        currentEvent.color = $('#edit-event-color').val();
        currentEvent.repeat = $('#edit-event-repeat').val();

        $('#calendar').fullCalendar('updateEvent', currentEvent);
        $('#editEventModal').modal('hide');
        updateEventLists();
    });

    // Handle event deletion
    $('#delete-event-btn').on('click', function() {
        $('#calendar').fullCalendar('removeEvents', currentEvent._id);
        $('#editEventModal').modal('hide');
        updateEventLists();
    });

    // Open edit modal with event data
    function openEditModal(event) {
        $('#editEventModal').modal('show');
        $('#edit-event-start').val(moment(event.start).format('DD-MM-YYYY HH:mm'));
        $('#edit-event-end').val(moment(event.end).format('DD-MM-YYYY HH:mm'));
        $('#edit-event-title').val(event.title);
        $('#edit-event-description').val(event.description);
        $('#edit-event-repeat').val(event.repeat || 'none');
        $('#edit-event-color').val(event.color);
        currentEvent = event;
    }

    // Update event lists
    function updateEventLists() {
        $('#today-events').empty();
        var events = $('#calendar').fullCalendar('clientEvents');
        var todayEvents = events.filter(function(event) {
            return moment(event.start).isSame(moment(), 'day');
        });

        todayEvents.sort(function(a, b) {
            return moment(a.start) - moment(b.start);
        });

        if (todayEvents.length === 0) {
            $('#today-events').append('<li>Сегодня события отсутствуют, можно отдохнуть</li>');
        } else {
            todayEvents.forEach(function(event) {
                var startTime = moment(event.start).format('HH:mm');
                var endTime = moment(event.end).format('HH:mm');
                var eventTimeRange = startTime + '-' + endTime;
                var eventColor = event.color ? 'style="color:' + event.color + '"' : '';

                var listItem = $('<li ' + eventColor + '>' + eventTimeRange + ' ' + event.title + '</li>');
                listItem.on('click', function() {
                    openEditModal(event);
                });
                $('#today-events').append(listItem);
            });
        }
    }

    // Initial update of event lists
    updateEventLists();
});
