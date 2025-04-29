$(document).ready(function(){
    // Afficher les organismes
    $("#btnAfficherOrganismes").click(function(){
        $.ajax({
            url: "/organismes/all",  // Route vers l'API qui renvoie les données des organismes
            method: "GET",
            success: function(response) {
                let tableBody = $("#tableOrganismes tbody");
                tableBody.empty();  // Vide la table avant de remplir les nouvelles données
                
                // Remplir la table avec les données des organismes
                response.forEach(function(organisme) {
                    let row = `<tr>
                        <td>${organisme.id}</td>
                        <td>${organisme.nom}</td>
                        <td>${organisme.adresse}</td>
                        <td>${organisme.email}</td>
                        <td>${organisme.telephone}</td>
                    </tr>`;
                    tableBody.append(row);  // Ajouter chaque ligne à la table
                });
                
                // Afficher la table après avoir ajouté les données
                $("#tableOrganismes").show();
            },
            error: function() {
                alert("Erreur lors de la récupération des données.");
            }
        });
    });

    // Cacher ou montrer la table
    $("#btnToggleTable").click(function(){
        $("#tableOrganismes").toggle();
    });
});