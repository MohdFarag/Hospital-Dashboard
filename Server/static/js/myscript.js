
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

    var category = document.getElementById("categ-"+list);
    if(category.lastElementChild != null){
        lastValue = category.lastElementChild.querySelector("#"+ list +"-id").value;
    }else{
        lastValue = 0;
    }
    addedValue = document.getElementById("add-"+list).value;
    if (list == "Model") {
        var e = document.getElementById("add-Model-equipment");
        var addedEquipment = e.options[e.selectedIndex].text;
    }
    
    if(addedValue == ""){
        return;
    }

    // Row
    //// <div id="row-{{equipment[0]}}" class="row mb-1">
    var row = document.createElement("div");
    row.setAttribute('class', "row mb-1");
    row.setAttribute('id', "row-" + list + "-"+(Number(lastValue) + 1));
    
    // Col
    ///// <div class="col-md-10">
    
    if (list=="Model") {
        var col1 = document.createElement("div");
        col1.setAttribute('class', "col-md-5");

        var col2 = document.createElement("div");
        col2.setAttribute('class', "col-md-5");
    }else{
        var col = document.createElement("div");
        col.setAttribute('class', "col-md-10");
    }

    // Input
    ///// <input id="equipment-{{equipment[0]}}" readonly type="text" value="{{ equipment[1] }}" class="form-control form-control-sm" />
    var input = document.createElement("input");
    if (list=="Model") {
        input.id = list + "-" + (Number(lastValue) + 1) + "-" + "1";
        input.name = list + "-" + (Number(lastValue) + 1) + "-" + "1";
    }else{
        input.id = list + "-" + (Number(lastValue) + 1);
        input.name = list + "-" + (Number(lastValue) + 1);
    }
    input.readOnly = true;
    input.type = "text";
    input.setAttribute("value", addedValue);
    input.classList = "form-control form-control-sm";

    if (list=="Model") {
        var select = document.createElement("select");
        select.id = list + "-" + (Number(lastValue) + 1) + "-" + "2";
        select.setAttribute("disabled", "true");
        select.classList = "form-control form-control-sm";
        
        equipmentsList = getEquipments()
        for (let i = 0; i < equipmentsList.length; i++) {
            let newOption = new Option(equipmentsList[i], equipmentsList[i]);
            if (equipmentsList[i] == addedEquipment) {
                newOption.selected = "selected";
            }
            select.add(newOption,undefined);
        }
    }
    
    // Input Hidden
    //// <input id="equipment-id" hidden type="text" value="{{ equipment[0] }}" />
    var inputHidden = document.createElement("input");
    inputHidden.type = "hidden";
    inputHidden.id = list + "-id";
    inputHidden.setAttribute("value", Number(lastValue) + 1);

    //// <div class="col-md-1">
    var col_add = document.createElement("div");
    col_add.setAttribute("class", "col-md-1");
    //// <a id="editIcon-{{equipment[0]}}" href="#" onclick="editItem('Equipment-{{equipment[0]}}')">
    var a_add = document.createElement("a");
    a_add.setAttribute("id", list + "-editIcon-" + inputHidden.value)
    a_add.href = "#";
    a_add.addEventListener("click", function(){ editItem(list + '-' + inputHidden.value); });
    //// <i class="dropdown-item-icon mdi mdi-border-color text-primary me-2"></i>
    var i_add = document.createElement("i");
    i_add.setAttribute("class", "dropdown-item-icon mdi mdi-border-color text-primary me-2");

    //// <a id="thump-{{equipment[0]}}" hidden href="#" onclick="doneEdit('Equipment-{{equipment[0]}}')">
    var a_done = document.createElement("a");
    a_done.setAttribute("id", list + "-thump-" + inputHidden.value)
    a_done.href = "#";
    a_done.hidden = true
    a_done.addEventListener("click", function(){ doneEdit(list + '-' + inputHidden.value); });
    //// <i class="dropdown-item-icon mdi mdi-thumb-up text-primary me-2"></i>
    var i_done = document.createElement("i");
    i_done.setAttribute("class", "dropdown-item-icon mdi mdi-thumb-up text-primary me-2");

    //// <div class="col-md-1">
    var col_delete = document.createElement("div");
    col_delete.setAttribute("class", "col-md-1");
    //// <a href="#" onclick="deleteItem('Equipment-{{equipment[0]}}')">
    var a_delete = document.createElement("a");
    a_delete.href = "#"
    a_delete.addEventListener("click", function(){ deleteItem(list + '-' + inputHidden.value); });
    //// <i class="dropdown-item-icon mdi mdi-delete text-primary me-2"></i>
    var i_delete = document.createElement("i");
    i_delete.setAttribute("class", "dropdown-item-icon mdi mdi-delete text-primary me-2");

    // Append
    category.appendChild(row);
    
    if (list=="Model") {
        row.appendChild(col1);
        col1.appendChild(input);
        row.appendChild(col2);
        col2.appendChild(select);
    }else{
        row.appendChild(col);
        col.appendChild(input);
    }
    
    row.appendChild(inputHidden);

    row.appendChild(col_add);
    col_add.appendChild(a_add);
    col_add.appendChild(a_done);
    a_add.appendChild(i_add)
    a_done.appendChild(i_done)

    row.appendChild(col_delete);
    col_delete.appendChild(a_delete);
    a_delete.appendChild(i_delete)

    document.getElementById("add-"+list).value = "";

    if(list == "Equipment"){
        var e = document.getElementById("add-Model-equipment");
        let newOption = new Option(addedValue, addedValue); 
        e.add(newOption,undefined);
    }

    updateNumberOfSections()
}

function editItem(list){
    list = list.split("-");
    id = list[1]
    list = list[0]

    a_editIcon = document.getElementById(list + "-editIcon-" + id);
    a_editIcon.hidden = true;
    a_thump = document.getElementById(list + "-thump-" + id);
    a_thump.hidden = false;

    if (list.includes("Model")) {
        input = document.getElementById(list + "-" + id + "-" + "1");
        select = document.getElementById(list + "-" + id + "-" + "2");
        select.removeAttribute("disabled");
    }else{
        input = document.getElementById(list + "-" + id);
    }
    input.readOnly = false;
}

function doneEdit(list){
    list = list.split("-");
    id = list[1]
    list = list[0]

    a_editIcon = document.getElementById(list + "-editIcon-"+id);
    a_editIcon.hidden = false;
    a_thump = document.getElementById(list + "-thump-" +id);
    a_thump.hidden = true;

    if (list.includes("Model")) {
        input = document.getElementById(list + "-" + id + "-" + "1");
        select = document.getElementById(list + "-" + id + "-" + "2");
        select.setAttribute("disabled", "true");
    }else{
        input = document.getElementById(list + "-" + id);
    }
    input.readOnly = true;
}


function deleteItem(list){
    list = list.split("-");
    id = list[1]
    list = list[0]
    
    row = document.getElementById("row" + "-" + list + "-" + id);
    row.remove()
    updateNumberOfSections()
}

function getEquipments(){
    var category = document.getElementById("categ-Equipment");
    Num = 0;
    if(category.lastElementChild != null){
        Num = Number(category.lastElementChild.querySelector("#Equipment-id").value);
    }

    equipmentsList = Array()
    for (let i = 1; i < Num+1; i++) {
        try {
            var input = document.getElementById("Equipment-"+i);
            equipmentsList.push(input.value);
        }
        catch(exceptionVar){

        }
    }

    return equipmentsList;
}

/////////////////////////////////////////////////// 
/// TODO :: UPDATE LIST OF EQUIPMENTS OF MODELS ///
///////////////////////////////////////////////////

function updateNumberOfSections(){
    // Equipment 
    equipmentDiv = document.getElementById("categ-Equipment");
    equipments = equipmentDiv.querySelectorAll("#Equipment-id");
    document.getElementById("num-equipment").value = equipments.length;

    // Model
    modelDiv = document.getElementById("categ-Model");
    models = modelDiv.querySelectorAll("#Model-id");
    document.getElementById("num-model").value = models.length;

    // Manufacturer
    ManufacturerDiv = document.getElementById("categ-Manufacturer");
    manufacturers = ManufacturerDiv.querySelectorAll("#Manufacturer-id");
    document.getElementById("num-manufacturer").value = manufacturers.length;

    // Location
    locationDiv = document.getElementById("categ-Location");
    locations = locationDiv.querySelectorAll("#Location-id");
    document.getElementById("num-location").value = locations.length;    
}