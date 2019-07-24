$(document).ready(function(){

/* Helpdesk - Homepage Ticket Submit Form  */

$("form#ticket_form").find("textarea").removeAttr("cols rows").attr("rows","5");

$("form#ticket_form").find("select, input, textarea").addClass("input-sm");
$("form#ticket_form").find(".btn").removeClass("input-sm");


/************************************************************************************* 
Filter Lists Filters and Setters Events 
url : tickets/
*************************************************************************************/

$("ul.filter-lists > li > a").click(function(){
	$("input#action").val(($(this).attr("href")).replace("#",""));
	$("#ticket_mass_update").submit();
})


/* PAGINATION SET PAGE SELECT/COMBO BOX SUBMIT */
$("form#pagination_select > select").change(function(e){
	e.preventDefault();
	$("form#pagination_select").submit();
})



});

function minimize(value, elem){
    
    if($(elem).attr("param") == 1){
    	$("#"+value).hide();
    	$(elem).children("i").removeClass().addClass("fa fa-caret-down")
    }
    else{
    	$("#"+value).show();
    	$(elem).children("i").removeClass().addClass("fa fa-caret-up")
    }
    $(elem).attr("param",1-$(elem).attr("param"));
}
