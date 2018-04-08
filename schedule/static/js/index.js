$(function () {
    $(".datepicker").datepicker();


    var today = new Date();
    var y = today.getFullYear();


    $('#exceptionDate').multiDatesPicker({
        numberOfMonths: [3,4],
        defaultDate: '4/1/'+y
    });


    $( ".createSchedule" ).submit(function( event ) {
        event.preventDefault();
        var exceptionDates = $('#exceptionDate').multiDatesPicker('getDates');
        var startDate = $("#startDate").val();
        var endDate = $("#endDate").val();

        var data ={start_date:startDate,end_date:endDate,exception_dates:exceptionDates};

        $.post( "/",data, function( data ) {
            $( ".result" ).html( data );
            window.location.href = '/schedule/';
        });

        console.log(exceptionDates);
        console.log(startDate);
        console.log(endDate);

      });


});