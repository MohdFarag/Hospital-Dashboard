function contractType(){
    var contract = document.getElementById('contract-type').value;
    var contract_start_date = document.getElementById('contract-start-date');
    var To = document.getElementById('To');
    var contract_end_date = document.getElementById('contract-end-date');
    var maintenance_contract_type = document.getElementById('maintenance-contract-type');

    if(contract==="Warranty") {
        maintenance_contract_type.style.display = 'none';
        contract_start_date.style.removeProperty('display');
        To.style.removeProperty('display');
        contract_end_date.style.removeProperty('display');
    }
    else if(contract==="Contract of Maintenance"){
        maintenance_contract_type.style.removeProperty('display');
        contract_start_date.style.removeProperty('display');
        To.style.removeProperty('display');
        contract_end_date.style.removeProperty('display');
    }
    else {
        contract_start_date.style.display = 'none';
        To.style.display = 'none';
        contract_end_date.style.display = 'none';
        maintenance_contract_type.style.display = 'none';
    }
};


function statusChange(statusValue){
    var PF_problem = document.getElementById('PF-problem');
    var NF_problem = document.getElementById('NF-problem');
    var problem_id = document.getElementById('problem-id')
    
    if (statusValue == "PF") {
        PF_problem.style.removeProperty('display');
        NF_problem.style.display = 'none';
        problem_id.style.removeProperty('display');
    }else if(statusValue == "NF"){
        NF_problem.style.removeProperty('display');
        PF_problem.style.display = 'none';
        problem_id.style.removeProperty('display');
    }else {
        PF_problem.style.display = 'none';
        NF_problem.style.display = 'none';
        problem_id.style.display = 'none';
    }
}
