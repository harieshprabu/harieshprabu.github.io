fetch('results.json')
    .then(response => response.json())
    .then(resultData => {
        let data = resultData;
        console.log(data);
        for (i in data) {
            //console.log(i);
            let record = data[i]
            console.log(record);
            date = data[i].date
            console.log(date);
            let center_container = $(`<div class="center-container"></div>`)
            $(center_container).css('background', '#DAEDC5')
            let center_title = $(`<div class="center-availability">${date}</div>`)
			let slot=""
			console.log(slot.length);
			//let slot=data[i].Court[0].slot
			
			for (j in data[i].Court) {				
                let tempslot= data[i].Court[j].slot
				if(slot.length=="0"){
					slot = tempslot
				}
				else{
				slot = slot + ',' + tempslot
                console.log("else");
				} 
				
				}
				
                        
            //let slot = data[i].Court[0].slot
            let center_availability = $(`<div class="center-title">${slot}</div>`)

            $(center_container).append(center_title)
            $(center_container).append(center_availability)
            $('#main-container').append(center_container)

            $('#main-container')
                .children()
                .sort((a, b) => {
                    return $(a).text().toUpperCase().localeCompare($(b).text().toUpperCase())
                })
                .each((a, b) => {
                    $('#main-container').append(b)
                })


        }

    })



fetch('update-time.txt')
    .then(response => response.text())
    .then(update_time => {
        $('#update-time').text(update_time)
    })