// General use scripts

// Change button color on select
    function selectButton(event) {
        const button = event.currentTarget;

        // remove all .active
        const buttons = document.querySelectorAll(".menu-button");
        buttons.forEach((button) => {
          button.classList.remove("active");
        });

        // add .active to button
        button.classList.add("active");
    }

// ----------------------------------------------------------------------------------------------------------------- //
// Changes div to show

    function toggleDivs(id) {
        var joined = document.getElementById("joined-bets");
        var invited = document.getElementById("invited-bets");

        if (id === "joined-bets") {
            joined.classList.remove("d-none");
            invited.classList.add("d-none")
        } else if (id === "invited-bets") {
            invited.classList.remove("d-none");
            joined.classList.add("d-none");
        }
    }

// ----------------------------------------------------------------------------------------------------------------- //
// Updates page by input on search WORKING MYBETS ONLY

    function filterSearch() {
        var input, filter, div, element_li, a, i, txtValue, id, btn1, btn2;

        // Variables FOR MY-BETS
        btn1 = document.getElementById("joined-btn");
        btn2 = document.getElementById("invited-btn");
        input = document.getElementById("search-input");
        filter = input.value.toUpperCase();
        div = document.getElementById(id);
        element_li = div.getElementsByClassName("card");

        // Change search targets by active button(translates to div on my-bets)
        if (btn1.classList.contains("active")) {
            id = "joined-bets"
        } else {
            id = "invited-bets"
        }

        // Hiding or showing elements responding to search
        for (i = 0; i < element_li.length; i++) {
            a = element_li[i].getElementsByTagName("h5")[0];
            txtValue = a.textContent || a.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                element_li[i].style.display = "";
            } else {
                element_li[i].style.display = "none";
            }
        }
    }
