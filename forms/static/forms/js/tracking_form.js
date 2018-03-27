// When the form is submitted we remove any values in the support fields if 
// the support required checkbox is not checked.
$('#tracking-form').submit(function(event) {
    var lab_support_required = $('#id_lab_support_required').is(':checked')
    var tutorial_support_required = $('#id_tutorial_support_required').is(':checked')
    if(!lab_support_required) {
        $('#id_lab_support_skills').val('')
        $('#id_lab_support_notes').val('')
    }
    if(!tutorial_support_required) {
        $('#id_tutorial_support_skills').val('')
        $('#id_tutorial_support_notes').val('')
    }
})

// When the page first loads we need to check to see whether the lab/tutorial
// support fields should be shown or collapsed.
$(document).ready(function(){
    var lab_support_required = $('#id_lab_support_required').is(':checked')
    var tutorial_support_required = $('#id_tutorial_support_required').is(':checked')
    if(lab_support_required) {
        $('#lab_support_collapse').addClass('show')
    }
    if(tutorial_support_required) {
        $('#tutorial_support_collapse').addClass('show')
    }
})