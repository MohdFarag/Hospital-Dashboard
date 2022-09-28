
function changeTerms(selector){
    input = document.getElementById("description")
    file = document.getElementById("description-file")
    textChangeTerms = document.getElementById("textChangeTerms")
    textChangeTerms.removeAttribute("onclick")

    if (selector=="file") {
        file.hidden = false
        input.hidden = true
        textChangeTerms.addEventListener("click", function(){ changeTerms("disc"); });
    }else{
        file.hidden = true
        input.hidden = false
        textChangeTerms.addEventListener("click", function(){ changeTerms("file"); });
    }
};

function prevImg(inputID,imgId){
    const [file] = document.getElementById(inputID).files
    if (file) {
        document.getElementById(imgId).src = URL.createObjectURL(file)
    }   
};

function changeQrInputToFile(selector){
    input = document.getElementById("code");
    qrcode = document.getElementById("qrcode");
    file = document.getElementById("qrcode-file");
    downloadQrcode = document.getElementById("downloadQrcode");
    QrcodeTextarea = document.getElementById("qrcodeTextArea");

    text = document.getElementById("textChangeQRcode");
    text.removeAttribute("onclick");

    if (selector=="file") {
        file.hidden = false;
        file.name = "qrcode";
        input.hidden = true;
        document.getElementById("qrcodeDiv").hidden = false;

        downloadQrcode.hidden = true;
        text.addEventListener("click", function(){ changeQrInputToFile("qrCode"); });
        text.innerHTML = "<b>OR</b> Generate QRCode ?" ;
        qrcode.innerHTML = "";
        QrcodeTextarea.name = "";
    }else{
        file.hidden = true;
        file.name = "";
        input.hidden = false;
        document.getElementById("qrcodeDiv").hidden = true;

        downloadQrcode.hidden = false;
        text.addEventListener("click", function(){ changeQrInputToFile("file"); });
        text.innerHTML = "<b>OR</b> Upload File ?" ;
        QrcodeTextarea.name = "qrcode"
    }

};

function contractTypes(){
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
};


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
    ///// <div class="col-md-10/5">
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
    if (list == "Model") {
        input.id = list + "-" + (Number(lastValue) + 1) + "-" + "1";
        input.name = list + "-" + (Number(lastValue) + 1) + "-" + "1";
    }else{
        input.id = list + "-" + (Number(lastValue) + 1);
        input.name = list + "-" + (Number(lastValue) + 1);
    }
    input.readOnly = true;
    input.type = "text";
    input.setAttribute("value", addedValue);
    if (list == "Equipment") {
        input.classList = "form-control form-control-sm equipment-input";
    }else{
        input.classList = "form-control form-control-sm";
    }

    if (list=="Model") {
        var select = document.createElement("select");
        select.id = list + "-" + (Number(lastValue) + 1) + "-" + "2";
        select.setAttribute("disabled", "true");
        select.classList = "form-control form-control-sm";
        
        equipmentsList = document.querySelectorAll(".equipment-input");
        for (let i = 0; i < equipmentsList.length; i++) {
            val = equipmentsList[i].value;
            let newOption = new Option(val, val);
            if (val == addedEquipment) {
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
        var selectList = document.querySelectorAll("select");
        for (let i = 0; i < selectList.length; i++) {
            let newOption = new Option(addedValue, addedValue); 
            selectList[i].add(newOption,undefined);
        }
    }

    // WRITE SQL STATEMENT OF INSERT PROCCESS
    statment = document.getElementById("statments");
    if (list.includes("Model")){        
        console.log(list + "-" + inputHidden.value + "-1")
        modelValue = document.getElementById(list + "-" + inputHidden.value + "-1").value;
        equipmentValue = document.getElementById(list + "-" + inputHidden.value + "-2").value;
        statment.value = statment.value + "INSERT INTO " + list + " VALUES (" + inputHidden.value + ",'" + addedValue + "'," + getEquipmentIdByName(addedEquipment) + ");";
    }else{
        value = document.getElementById(list + "-" + inputHidden.value).value;
        statment.value = statment.value + "INSERT INTO " + list + " VALUES (" + inputHidden.value + ",'" + addedValue + "');";
    }
    
    updateNumberOfSections()
};

prevValue = ""
function editItem(list){
    list = list.split("-");
    id = list[1]
    list = list[0]

    if (list=="Equipment") {
        prevValue = document.getElementById(list + "-" + id).value;
    }

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
};

function doneEdit(list){
    list = list.split("-");
    id = list[1]
    list = list[0]
    
    // WRITE SQL STATEMENT OF DELETE PROCCESS
    statment = document.getElementById("statments");
    if (list.includes("Model")){        
        modelValue = document.getElementById(list + "-" + id + "-1").value;
        equipmentValue = document.getElementById(list + "-" + id + "-2").value;
        statment.value = statment.value + "UPDATE " + list + " SET Model_name='" + modelValue + "', Equipment_name='" + equipmentValue + "' WHERE " + list + "_id="+ id + ";";
    }else{
        value = document.getElementById(list + "-" + id).value;
        statment.value = statment.value + "UPDATE " + list + " SET " + list + "_name='" + value + "' WHERE " + list + "_id="+ id + ";";
    }

    // EDIT FIELD
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

    if(list == "Equipment"){
        var selectList = document.querySelectorAll("select");
        for (let i = 0; i < selectList.length; i++) {
            options = selectList[i].querySelectorAll("option");
            for (let i = 0; i < options.length; i++) {
                if(options[i].text == prevValue){
                    options[i].value = value;
                    options[i].text = value;
                }
            }
        }
    }
};

function deleteItem(list){
    // SEPERATE LIST TO ID AND CATEGORY NAME
    list = list.split("-");
    id = list[1]
    list = list[0]

    // WRITE SQL STATEMENT OF DELETE PROCCESS
    statment = document.getElementById("statments");
    if (list.includes("Model")){
        value = document.getElementById(list + "-" + id + "-1").value;
    }else{
        value = document.getElementById(list + "-" + id).value;
    }
    statment.value = statment.value + "DELETE FROM " + list + " WHERE " + list + "_name='" + value + "';";

    // REMOVE HTML ELEMENT
    row = document.getElementById("row" + "-" + list + "-" + id);
    row.remove()

    if(list == "Equipment"){
        var selectList = document.querySelectorAll("select");
        for (let i = 0; i < selectList.length; i++) {
            options = selectList[i].querySelectorAll("option");
            for (let i = 0; i < options.length; i++) {
                if(options[i].text == value){
                    options[i].remove()
                }
            }
        }
    }

    updateNumberOfSections()
};

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
};

function getEquipmentIdByName(name){
    inputs = document.querySelectorAll(".equipment-input");
    id = 0;
    for (let i = 0; i < inputs.length; i++) {
        if (name == inputs[i].value) {
            id = inputs[i].parentElement.parentElement.querySelector("#Equipment-id").value
        }
    }
    return id;
};

