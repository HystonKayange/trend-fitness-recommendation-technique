function displayLoader(timer){
    document.querySelector("#processing").classList.remove('hidden-item')
        setTimeout(()=>{          
            document.querySelector("#processing").classList.add('hidden-item')
        }, timer)
}

function loadNewData(hide, show){
    for(let i of hide){
        i.classList.remove('show')
        i.classList.add('hidden')
    }  

    displayLoader(3000)

    for(let i of show){
        i.classList.add('show')
        i.classList.remove('hidden')
    }
}