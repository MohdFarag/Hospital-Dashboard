
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


function addItem(list){

    if (list == "Equipment") {
        var categ_equipment = document.getElementById("categ-equipment");
        lastValue = categ_equipment.lastElementChild.querySelector("#equipment-id").value;
        addedValue = document.getElementById("add-equipment").value
        
        if(addedValue == ""){
            return;
        }
        // Row
        var row = document.createElement("div");
        row.setAttribute('class', "row mb-1");
        
        // Col
        var col = document.createElement("div");
        col.setAttribute('class', "col-md-10");
        
        // Input
        var input = document.createElement("input");
        input.id = "equipment-" + (Number(lastValue) + 1)
        input.readOnly = true;
        input.type = "text";
        input.setAttribute("value", addedValue);
        input.classList = "form-control form-control-sm";
        
        var inputHidden = document.createElement("input");
        inputHidden.hidden = true;
        inputHidden.type = "text";
        inputHidden.id = "equipment-id"
        inputHidden.setAttribute("value", Number(lastValue) + 1);

        var col_add = document.createElement("div");
        col_add.setAttribute("class", "col-md-1");
        var a_add = document.createElement("a");
        a_add.href = "#";
        a_add.addEventListener("click", function(){ editItem('Equipment-'+inputHidden.value); });
        var i_add = document.createElement("i");
        i_add.setAttribute("class", "dropdown-item-icon mdi mdi-border-color text-primary me-2");

        var col_delete = document.createElement("div");
        col_delete.setAttribute("class", "col-md-1");
        var a_delete = document.createElement("a");
        a_delete.href = "#"
        a_delete.addEventListener("click", function(){ deleteItem('Equipment-'+inputHidden.value); });
        var i_delete = document.createElement("i");
        i_delete.setAttribute("class", "dropdown-item-icon mdi mdi-delete text-primary me-2");

        // Add
        categ_equipment.appendChild(row);
        
        row.appendChild(col);
        col.appendChild(input);

        row.appendChild(inputHidden);

        row.appendChild(col_add);
        col_add.appendChild(a_add);
        a_add.appendChild(i_add)

        row.appendChild(col_delete);
        col_delete.appendChild(a_delete);
        a_delete.appendChild(i_delete)

        document.getElementById("add-equipment").value = "";
        
    }else if(list == "Model"){
        var categ_model = document.getElementById("categ-model");

    }else if(list == "Manufacturer"){
        var categ_manufacturer = document.getElementById("categ-manufacturer");

    }else if(list == "Location"){
        var categ_location = document.getElementById("categ-location");

    }
}

function editItem(list){
    id = list.slice(-1);
    input = document.getElementById("equipment-"+id);
    input.readOnly = false;

    if (list.includes("Equipment")) {
        var categ_equipment = document.getElementById("categ-equipment");

    }else if(list.includes("Model")){
        var categ_model = document.getElementById("categ-model");

    }else if(list.includes("Manufacturer")){
        var categ_manufacturer = document.getElementById("categ-manufacturer");

    }else if(list.includes("Location")){
        var categ_location = document.getElementById("categ-location");

    }
}

function deleteItem(list){
    id = list.slice(-1);

    if (list.includes("Equipment")) {
        var categ_equipment = document.getElementById("categ-equipment");

    }else if(list.includes("Model")){
        var categ_model = document.getElementById("categ-model");

    }else if(list.includes("Manufacturer")){
        var categ_manufacturer = document.getElementById("categ-manufacturer");

    }else if(list.includes("Location")){
        var categ_location = document.getElementById("categ-location");

    }
}
