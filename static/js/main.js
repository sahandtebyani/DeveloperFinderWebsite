//GET SEARCH FORM AND PAGE LINKS

let searchForm = document.getElementById('searchForm')
let pageLink = document.getElementsByClassName('page-link')

// ENSURE SEARCH FORM EXISTS
if (searchForm) {
    for(let i=0; pageLink.length > 1; i++){
        pageLink[i].addEventListener('click', function (e){
            e.preventDefault()

            //GET DATA ATTRIBUTE
            let page = this.dataset.page

            //ADD HIDDEN SEARCH INPUT TO FORM
            searchForm.innerHTML += `<input value=${page} name='page' hidden/>`

            //SUBMIT FORM
            searchForm.submit()
        })
    }
}
