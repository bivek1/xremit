
  $('#flightInfo').hide()
  $('#reason').hide()
  $('#review2').hide()
  $('#review3').hide()
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
        // $('#receipt').hide().fadeOut(1000)
        // $('#flightInfo').hide()
        // $('#buttonInfo').hide()
        // $('#tripInfo').hide()
        // $('#complete').show()
        // $('#trip').addClass('completed')
        // $('#pay').addClass('active')
        $('#receipt').hide().fadeOut(1000)
        $('#flightInfo').hide()
        $('#buttonInfo').hide()
        $('#review2').hide()
        $('#review3').show().fadeIn(1000)
  })
  $('#procees_five').click(function(){
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
        $('#complete').hide()
        $('#buttonInfo').show()
        $('#tripInfo').hide().fadeOut(1000);
  }

  function switchAmount(){
        $('#flightInfo').show()
        $('#complete').hide()
        $('#buttonInfo').hide()
        $('#tripInfo').hide().fadeOut(1000);
        $('#info').removeClass('active')
        $('#info').addClass('completed')        
        $('#book').addClass('active')
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
                    var ansdata = '<div class="col-6 mt-2 p-2 banN" onclick=senddata(this,'+ bank[i]['pk']+ ')> <div class="bankhere p-2"><p class="text-secondary p-0 m-0">Bank Name:</p><p class="text-dark p-0 m-0" id="bankNameList">'+bank[i]['fields']['bank_name']+'</p><div class="d-flex justify-content-between mt-2"><p class="text-secondary"> Account Number:</p> <p class="text-secondary" id="bankNumberList">'+bank[i]['fields']['account_number']+'</p> </div> <div class="d-flex justify-content-between"> <p class="text-secondary"> Account Name: </p> <p class="text-secondary" id="bankSwiftList">'+bank[i]['fields']['account_name']+'</p> </div> </div></div>'
                    console.log(ansdata)
                    $('#bankList').append(ansdata)
                    // console.log(bank[i]['fields']['account_name'] + bank[i]['fields']['account_number']+ bank[i]['fields']['bank_name'] + bank[i]['fields']['country']+ bank[i]['fields']['swift_code'])
                }
            }
      });
  

        $('#reason').show().slideDown(1000);
      
        
        // Add border to the clicked div
        element.classList.add('selected');
    }

    

    function addSendPurpose(em){
        $('#id_sending_purpose').val(em.val)
    }
    function addFund(em){
        $('#id_source_of_fund').val(em.val)
    }






    currency_rate = '{{default.currecy_rate}}'
    receiving_rate = 0
    fee = '{{default.conversion_rate}}'
    cur_sign = '{{default.currecy_sign}}'
    re_cur_sign = '{{rec_default.currecy_sign}}'
    converting_amt = 0
    sending_amt = document.getElementById('fee').value
    receiving_amt = 0 
    receipient_id = 0
    $('#id_sending_currency').val('{{default.id}}')

    function checkCurrency(){
        sending_amt = document.getElementById('sendingMoney').value
        console.log(sending_amt)
        
        // $('#converting_amt').text(converting_amt +"  " + cur_sign)
        if (sending_amt != ''){
            converting_amt =parseFloat(sending_amt) - parseFloat(fee)
        }
        
        $('#converting_amt').text(converting_amt +"  " + cur_sign  )
        $('#rate').text(parseFloat(receiving_rate).toFixed(2) + "  " + re_cur_sign) 
        $('#fee').text(parseFloat(fee).toFixed(2)  + "  " + cur_sign)
        receiving_amt = (converting_amt / currency_rate) * receiving_rate;
        recieving_two_digit_nuumber = parseFloat(receiving_amt).toFixed(2)
        
        $('#gets').val(recieving_two_digit_nuumber)
        
        $('#r_sent_money').text(sending_amt + "  " + cur_sign)
        $('#r_commision').text("-" + parseFloat(fee).toFixed(2) + "  " + cur_sign)
        $('#r_covert').text(converting_amt +"  " + cur_sign)
        $('#r_rate').text(parseFloat(receiving_rate).toFixed(2) + "  " + re_cur_sign)
        $('#receiving_amt_id').text(parseFloat(receiving_amt).toFixed(2) + " " + re_cur_sign)

        $('#next_sent_money').text(sending_amt + "  " + cur_sign)
        $('#next_commision').text("-" + parseFloat(fee).toFixed(2) + "  " + cur_sign)
        $('#next_convert').text(converting_amt +"  " + cur_sign)
        $('#next_rate').text(parseFloat(receiving_rate).toFixed(2) + "  " + re_cur_sign)
        $('#next_receiving_amt_id').text(parseFloat(receiving_amt).toFixed(2) + " " + re_cur_sign)

        $('#id_sent').val(parseFloat(sending_amt).toFixed(2))
        $('#id_received').val(parseFloat(receiving_amt).toFixed(2))
        $('#id_converting_rate').val(parseFloat(currency_rate).toFixed(2))
        $('#id_fee').val(parseFloat(fee).toFixed(2))
        $('#id_customer').val('{{customer.id}}')

    }


    function changeState(id, src, sign){
        $('#sending_currency_sign').text(sign);
        path ='/media/' + src
        $('#sending_currency_img').attr('src', path);
        $('#id_sending_currency').val(parseInt(id))
        $.ajax({
            type: 'POST',
            url: '{%url "customer:changeCurone"%}', // Replace with the actual URL of your view
            data: {
                'id': id, // Send the data as a key-value pair
                'csrfmiddlewaretoken': '{{ csrf_token }}' // Include the CSRF token for security
            },
            success: function(response) {
               
                currency_rate =parseFloat(response.currency_rate).toFixed(2) 
                fee = parseFloat(response.fee).toFixed(2)
                cur_sign = response.cur_sign
                checkCurrency()
            
            }
      });
  
    }


    function changeStateTwo(id, src, sign){
        
        $('#recv_currency_sign').text(sign);
        path ='/media/' + src
        $('#recv_currency_img').attr('src', path);
        $('#id_receiving_currency').val(parseInt(id))
        $.ajax({
            type: 'POST',
            url: '{%url "customer:changeCurone"%}', // Replace with the actual URL of your view
            data: {
                'id': id, // Send the data as a key-value pair
                'csrfmiddlewaretoken': '{{ csrf_token }}' // Include the CSRF token for security
            },
            success: function(response) {
                receiving_rate =parseFloat(response.currency_rate).toFixed(2) 
                fee = parseFloat(response.fee).toFixed(2)
                re_cur_sign = response.cur_sign
               
                checkCurrency()
            
            }
      });
  
    }

    function senddata(elem, id){
        
        $('#id_bank').val(id)
        // // Remove border from all divs
        $.ajax({
            type: 'POST',
            url: '{%url "customer:getBank"%}', // Replace with the actual URL of your view
            dataType: 'json',
            data: {
                'id': id, // Send the data as a key-value pair
                'csrfmiddlewaretoken': '{{ csrf_token }}' // Include the CSRF token for security
            },
            success: function(data) {
                console.log(data.repName)
                console.log(data.account_name)
                $('#id_receiving_currency').val(data.id)
                $('#recpNamedd').text(data.repName)
                $('#bankName').text(data.bank_name)
                $('#bankAccount').text(data.account_number)
                $('#accountName').text(data.account_name)
                $('#recName1').text(data.repName)
                $('#bankName1').text(data.bank_name)
                $('#bankAccount1').text(data.account_number)
                $('#accountName1').text(data.account_name)
                re_cur_sign = data.currecy_sign
                receiving_rate = data.currency_rate
                fee = data.conversion_rate
                
                $('#recv_currency_sign').text(re_cur_sign);
                // console.log(data.img)
                path = data.img
                $('#recv_currency_img').attr('src', path);
                $('#id_sending_currency').val('{{default.id}}')
                checkCurrency()
            }
        })

        const ss = document.getElementsByClassName('banN');
        for (let i = 0; i < ss.length; i++) {
            ss[i].classList.remove('bankselected');
        }
        elem.classList.add('bankselected');
       
    }
   
