function supprimerFormation(id) {
    if (confirm("Voulez-vous vraiment supprimer cette formation ?")) {
        $.post(`/formations/delete/${id}`, function(response) {
            if (response.success) {
                $(`#formation-row-${id}`).remove();
            } else {
                alert("Erreur lors de la suppression de la formation.");
            }
        }).fail(function() {
            alert("Erreur serveur lors de la suppression.");
        });
    }
}

function supprimerOrganisme(id) {
    if (confirm("Voulez-vous vraiment supprimer cet organisme ?")) {
        $.post(`/organismes/delete/${id}`, function(response) {
            if (response.success) {
                $(`#organisme-row-${id}`).remove();
            } else {
                alert("Erreur lors de la suppression de l'organisme.");
            }
        }).fail(function() {
            alert("Erreur serveur lors de la suppression.");
        });
    }
}

$(document).ready(function(){
    // Afficher les organismes
    $("#btnAfficherOrganismes").click(function(){
        $.ajax({
            url: "/organismes/all",
            method: "GET",
            success: function(response) {
                let tableBody = $("#tableOrganismes tbody");
                tableBody.empty();
                
                response.forEach(function(organisme) {
                    let row = `<tr id="organisme-row-${organisme.id}">
                        <td>${organisme.id}</td>
                        <td>${organisme.nom}</td>
                        <td>${organisme.adresse}</td>
                        <td>${organisme.email}</td>
                        <td>${organisme.telephone}</td>
                        <td>
                            <button class="btn btn-danger btn-sm" onclick="supprimerOrganisme(${organisme.id})">
                                🗑
                            </button>
                        </td>
                    </tr>`;
                    tableBody.append(row);
                });
                $("#tableOrganismes").show();
            },
            error: function() {
                alert("Erreur lors de la récupération des données.");
            }
        });
    });

    $("#btnToggleTableOrga").click(function(){
        $("#tableOrganismes").toggle();
    });

    // Afficher les formations
    $("#btnAfficherFormations").click(function(){
        $.ajax({
            url: "/formations/all",
            method: "GET",
            success: function(response) {
                let tableBody = $("#tableFormations tbody");
                tableBody.empty();

                response.forEach(function(formation) {
                    let row = `<tr id="formation-row-${formation.id}">
                        <td>${formation.id}</td>
                        <td>${formation.nom}</td>
                        <td>${formation.type}</td>
                        <td>${formation.description}</td>
                        <td>${formation.duree}</td>
                        <td>${formation.lieu}</td>
                        <td>${formation.prix}</td>
                        <td>
                            <button class="btn btn-danger btn-sm" onclick="supprimerFormation(${formation.id})">
                                🗑
                            </button>
                        </td>
                    </tr>`;
                    tableBody.append(row);
                });
                $("#tableFormations").show();
            },
            error: function() {
                alert("Erreur lors de la récupération des données.");
            }
        });
    });

    $("#btnToggleTableForma").click(function(){
        $("#tableFormations").toggle();
    });
});
