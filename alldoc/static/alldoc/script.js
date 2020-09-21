$(document).ready(function() {
    $('.table-wow').DataTable( {
        pageLength: 10,
        dom: 'Bfrt<"bottom"lip>',
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5'
        ]
    } );
} );