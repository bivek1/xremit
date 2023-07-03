
  $('#flightInfo').hide()
  $('#reason').hide()
  $('#tripInfo').hide()
  $('#complete').hide()
  $('#procees_one').click(function(){
    
      if(document.getElementById('sendingMoney').value == '' || document.getElementById('gets').value ==""){
          $('#infoerror').text("Enter all Fields Correctly") 
  
          $('#infoerror').show()
          

      }
      else{
          
        $('#infoerror').hide()
        $('#flightInfo').show().fadeIn(1000);
        $('#buttonInfo').hide()
        $('#book').addClass('active')
        $('#info').removeClass('active')
        $('#info').addClass('completed')

      }
    
  })
  
  $('#procees_two').click(function(){
    
        $('#flightInfo').hide()
        $('#buttonInfo').hide()
        // $('#tripInfo').show()
        $('#book').removeClass('active')
        $('#info').removeClass('active')
        
        $('#trip').addClass('active')
        $('#trip').addClass('completed')
    
  })

  $('#procees_three').click(function(){
        $('#flightInfo').hide()
        $('#buttonInfo').hide()
        $('#tripInfo').hide()
        $('#complete').show()
        $('#book').removeClass('active')
        $('#info').removeClass('active')
        $('#pay').addClass('active')
        $('#pay').addClass('completed')
  })





    currency_rate = '{{default.currecy_rate}}'
    fee = '{{default.conversion_rate}}'
    cur_sign = '{{default.currecy_sign}}'
    converting_amt = 0
    sending_amt = document.getElementById('fee').value
    receiving_amt = 0 


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
    }


    function changeState(id, src, sign){

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
                $('#converting_amt').text(converting_amt +"  " + cur_sign  )
                $('#rate').text(currency_rate + "  " + cur_sign) 
                $('#fee').text(fee + "  " + cur_sign)
                receiving_amt = parseFloat(currency_rate) * converting_amt
                console.log(receiving_amt)
                $('#gets').val(receiving_amt)
            }
      });
  
    }



    function changeStateTwo(id, src, sign){
        console.log(sign)
        $('#recv_currency_sign').text(sign);
        path ='/media/' + src
        $('#recv_currency_img').attr('src', path);
        console.log(sign)
  
    }


    function toggleBorder(element) {
        // Remove border from all divs
        $('#reason').hide().slideDown(1000);
        const boxes = document.getElementsByClassName('box');
        for (let i = 0; i < boxes.length; i++) {
            boxes[i].classList.remove('selected');
        }
    
       
      
        $('#reason').show().slideDown(1000);
      
        
        // Add border to the clicked div
        element.classList.add('selected');
    }



