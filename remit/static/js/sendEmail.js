
// $('#sendEmail').hide()
// $('#customerList').hide()
$('#recipientList').hide()
$('#agentList').hide()

function selectEmail(elem, type){
    console.log(elem)
    console.log(type)
    if(type == 'customer'){
        $('#sendEmail').hide()
        $('#customerList').show().slideDown(1000);
        $('#recipientList').hide()
        $('#agentList').hide()
        $('#sendEmail').show().slideDown(1000)
    }   
    else if (type == 'agent'){
        $('#sendEmail').hide()
        $('#agentList').show().slideDown(1000);
        $('#customerList').hide()
        $('#recipientList').hide()
        $('#sendEmail').show()
    }else{
        $('#sendEmail').hide()
        $('#recipientList').show().slideDown(1000);
        $('#customerList').hide()
        $('#agentList').hide()
        $('#sendEmail').show()
    }
    
    const boxes = document.getElementsByClassName('box');
    for (let i = 0; i < boxes.length; i++) {
        boxes[i].classList.remove('selected');
    }
    elem.classList.add('selected');
}

const checkbox = document.getElementById('allCustomer');
const select = document.getElementById('customer');

checkbox.addEventListener('change', function() {
if (this.checked) {
    select.disabled = true;
} else {
    select.disabled = false;
}
});


const checkboxs = document.getElementById('allAgent');
const selects = document.getElementById('agent');

checkboxs.addEventListener('change', function() {
if (this.checked) {
    selects.disabled = true;
} else {
    selects.disabled = false;
}
});

const checkboxss = document.getElementById('allRecipient');
const selectss = document.getElementById('recipient');

checkboxss.addEventListener('change', function() {
if (this.checked) {
    selectss.disabled = true;
} else {
    selectss.disabled = false;
}
});

group = "Individual"

function getCustomerValue(elem){
    $('#id_customer').val(elem.value)
    group = "Individual"
    document.getElementById('id_group').value = group
}

function getCustomerValueAll(elem){
    group = "Customer"
    document.getElementById('id_group').value = group
}


function getReceiptionValue(elem){
    $('#id_reciptient').val(elem.value)
    group = "Individual"
    document.getElementById('id_group').value = group
}

function getReceiptionValueAll(elem){
    group = "Recipient"
    document.getElementById('id_group').value = group 
}


function getAgentValue(elem){
    $('#id_agent').val(elem.value)
    group = "Individual"
    document.getElementById('id_group').value = group
}


function getAgentValueAll(elem){
    group = "Agent"
    document.getElementById('id_group').value = group
}