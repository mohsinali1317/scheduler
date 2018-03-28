$(function () {
    $(".datepicker").datepicker();


    var today = new Date();
    var y = today.getFullYear();


    $('#exceptionDate').multiDatesPicker({
        numberOfMonths: [3,4],
        defaultDate: '5/1/'+y
    });


    $( ".createSchedule" ).submit(function( event ) {
        event.preventDefault();
        var exceptionDates = $('#exceptionDate').multiDatesPicker('getDates');
        var startDate = $("#startDate").val();
        var endDate = $("#endDate").val();
        console.log(exceptionDates);
        console.log(startDate);
        console.log(endDate);

      });


});