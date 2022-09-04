
function contractType(){
    var contract = document.getElementById('contract-type').value;
    if(contract==="Warranty") {
        $("#contract-start-date").show();
        $("#To").show();
        $("#contract-end-date").show();
        $("#maintenance-contract-type").hide();
    }
    else if(contract==="Contract of Maintenance"){
        $("#maintenance-contract-type").show();
        $("#contract-start-date").show();
        $("#To").show();
        $("#contract-end-date").show();
    }
    else {
        $("#contract-start-date").hide();
        $("#To").hide();
        $("#contract-end-date").hide();
        $("#maintenance-contract-type").hide();
    }
};