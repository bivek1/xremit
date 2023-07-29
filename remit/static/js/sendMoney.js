$('#flightInfo').hide()
$('#reason').hide()
$('#review2').hide()
$('#tripInfo').hide()
$('#complete').hide()
$('#procees_one').click(function(){
      $('#flightInfo').show()
      $('#buttonInfo').hide()
      $('#info').removeClass('active')
      $('#info').addClass('completed')        
      $('#book').addClass('active')
})

$('#procees_two').click(function(){

  if(document.getElementById('sendingMoney').value == '' || document.getElementById('gets').value ==""){
        $('#infoerror').text("Enter all Fields Correctly") 

        $('#infoerror').show()
    }
    else{
        
      $('#infoerror').hide()
      $('#flightInfo').hide()
      $('#book').addClass('completed')
      $('#tripInfo').show().fadeIn(1000);
      $('#trip').addClass('active')

    }

})


$('#procees_three').click(function(){
      $('#receipt').hide().fadeOut(1000)
      $('#flightInfo').hide()
      $('#buttonInfo').hide()
      
      $('#review2').show().fadeIn(1000)
      // $('#complete').show()

})
$('#procees_four').click(function(){
      $('#receipt').hide().fadeOut(1000)
      $('#flightInfo').hide()
      $('#buttonInfo').hide()
      $('#tripInfo').hide()
      $('#complete').show()
      $('#trip').addClass('completed')
      $('#pay').addClass('active')
})


function switchReciptient(){
      $('#flightInfo').hide()
      $('#buttonInfo').show()
      $('#tripInfo').hide().fadeOut(1000);
}

function switchAmount(){
      $('#flightInfo').show()
      $('#buttonInfo').hide()
      $('#tripInfo').hide().fadeOut(1000);
      $('#info').removeClass('active')
      $('#info').addClass('completed')        
      $('#book').addClass('active')
}



  currency_rate = '{{default.currecy_rate}}'
  fee = '{{default.conversion_rate}}'
  cur_sign = '{{default.currecy_sign}}'
  converting_amt = 0
  sending_amt = document.getElementById('fee').value
  receiving_amt = 0 
  receipient_id = 0
  $('#id_sending_currency').val(parseInt('{{default.id}}'))
  $('#id_receiving_currency').val(parseInt('{{default.id}}'))


  function checkCurrency(){
      sending_amt = document.getElementById('sendingMoney').value
      console.log(sending_amt)
      converting_amt =parseFloat(sending_amt) - parseFloat(fee)
      $('#converting_amt').text(converting_amt +"  " + cur_sign  )
      $('#rate').text(currency_rate + "  " + cur_sign) 
      $('#fee').text(fee + "  " + cur_sign)
      receiving_amt = parseFloat(currency_rate) * converting_amt
      console.log(receiving_amt)
      $('#gets').val(receiving_amt)
      
      $('#r_sent_money').text(sending_amt + "  " + cur_sign)
      $('#r_commision').text("-" + fee + "  " + cur_sign)
      $('#r_covert').text(converting_amt +"  " + cur_sign)
      $('#r_rate').text(currency_rate + "  " + cur_sign)

      $('#id_customer').val('{{customer.id}}')
      
      $('#r_covert').text(converting_amt +"  " + cur_sign)
      $('#r_rate').text(currency_rate + "  " + cur_sign)

      $('#id_sent').val(sending_amt)
      $('#id_received').val(receiving_amt)
      $('#id_converting_rate').val(currency_rate)
      $('#id_fee').val(fee)

  }


  function changeState(id, src, sign){
      $('#id_sending_currency').val = id
      $('#sending_currency_sign').text(sign);
      path ='/media/' + src
      $('#sending_currency_img').attr('src', path);

      $.ajax({
          type: 'POST',
          url: '{%url "customer:changeCurone"%}', // Replace with the actual URL of your view
          data: {
              'id': id, // Send the data as a key-value pair
              'csrfmiddlewaretoken': '{{ csrf_token }}' // Include the CSRF token for security
          },
          success: function(response) {
              console.log(response.currency_rate)
              console.log(response.fee)
              console.log(response.cur_sign)
              currency_rate = response.currency_rate
              fee = response.fee
              cur_sign = response.cur_sign
            
              sending_amt = document.getElementById('sendingMoney').value
              console.log(sending_amt)
              converting_amt =parseFloat(sending_amt) - parseFloat(fee)
              $('#converting_amt').text(converting_amt +"  " + response.cur_sign  )
              $('#rate').text(currency_rate + "  " + response.cur_sign) 
              $('#fee').text(fee + "  " + response.cur_sign)
              receiving_amt = parseFloat(currency_rate) * converting_amt
              console.log(receiving_amt)
              $('#gets').val(receiving_amt)
  
                // for form
              $('#id_sent').val(sending_amt)
             
              $('#id_received').val(receiving_amt)
              $('#id_converting_rate').val(currency_rate)
              $('#id_fee').val(fee)
          
          }
    });

  }

  function changeStateTwo(id, src, sign){
      console.log(id, sign)
      $('#id_receiving_currency').val = id
      $('#recv_currency_sign').text(sign);
      path ='/media/' + src
      $('#recv_currency_img').attr('src', path);
      console.log(sign)

  }

  function toggleBorder(element, id) {
      console.log(id)
      receipient_id = id
      $('#id_recipient').val(id)
      // Remove border from all divs
      $('#reason').hide().slideDown(1000);
      const boxes = document.getElementsByClassName('box');
      for (let i = 0; i < boxes.length; i++) {
          boxes[i].classList.remove('selected');
      }

      $.ajax({
          type: 'POST',
          url: '{%url "customer:findBank"%}', // Replace with the actual URL of your view
          dataType: 'json',
          data: {
              'id': id, // Send the data as a key-value pair
              'csrfmiddlewaretoken': '{{ csrf_token }}' // Include the CSRF token for security
          },
          success: function(data) {
              bank = JSON.parse(data)
              console.log(bank)
              // console.log(response.bank)
              $('.banN').remove()
              
              for(i in bank){
                  var ansdata = '<div class="col-6 mt-2 p-2 banN" onclick=senddata(this,'+bank[i]['pk']+','+'"'+bank[i]['fields']['account_name']+'"'+','+'"'+bank[i]['fields']['account_number']+'"'+','+'"'+bank[i]['fields']['bank_name']+'"'+','+'"'+bank[i]['fields']['country']+'"'+','+'"'+bank[i]['fields']['swift_code']+'"'+')> <div class="bankhere p-2"><p class="text-secondary p-0 m-0">Bank Name:</p><p class="text-dark p-0 m-0" id="bankNameList">'+bank[i]['fields']['bank_name']+'</p><div class="d-flex justify-content-between mt-2"><p class="text-secondary"> Account Number:</p> <p class="text-secondary" id="bankNumberList">'+bank[i]['fields']['account_number']+'</p> </div> <div class="d-flex justify-content-between"> <p class="text-secondary"> Account Name: </p> <p class="text-secondary" id="bankAccountList"> </p> </div> <div class="d-flex justify-content-between"> <p class="text-secondary"> Account Name: </p> <p class="text-secondary" id="bankSwiftList">'+bank[i]['fields']['account_name']+'</p> </div> </div></div>'
                  console.log(ansdata)
                  $('#bankList').append(ansdata)
                  console.log(bank[i]['fields']['account_name'] + bank[i]['fields']['account_number']+ bank[i]['fields']['bank_name'] + bank[i]['fields']['country']+ bank[i]['fields']['swift_code'])
              }
          }
    });


      $('#reason').show().slideDown(1000);
    
      
      // Add border to the clicked div
      element.classList.add('selected');
  }

  function senddata(elem, id, account, number, bank, country, swift){
     
      $('#id_bank').val(id)
      // // Remove border from all divs
   
      const ss = document.getElementsByClassName('bankhere');
      for (let i = 0; i < ss.length; i++) {
          ss[i].classList.remove('selected');
      }
      elem.classList.add('selected');
      console.log(id, account,number, bank, country, swift)
  }
