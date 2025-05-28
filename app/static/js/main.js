function supprimerFormation(id) {
    if (confirm("Voulez-vous vraiment supprimer cette formation ?")) {
        $.post(`/formations/delete/${id}`, function(response) {
            $(`#formation-row-${id}`).remove();
            $("#countFormations").text($("#tableFormations tbody tr").length);
        }).fail(() => alert("Erreur serveur lors de la suppression."));
    }
}

function supprimerOrganisme(id) {
    if (confirm("Voulez-vous vraiment supprimer cet organisme ?")) {
        $.post(`/organismes/delete/${id}`, function(response) {
            $(`#organisme-row-${id}`).remove();
            $("#countOrganismes").text($("#tableOrganismes tbody tr").length);
        }).fail(() => alert("Erreur serveur lors de la suppression."));
    }
}

function exportTable(tableId, format, type) {
    const table = document.getElementById(tableId);
    const rows = Array.from(table.querySelectorAll("tr"));
    const headers = Array.from(rows[0].querySelectorAll("th")).map(th => th.innerText).filter(h => h !== "Action");

    const data = rows.slice(1).map(row =>
        Array.from(row.querySelectorAll("td")).slice(0, headers.length).map(cell => cell.innerText)
    );

    const date = new Date();
    const dateString = date.toISOString().slice(0, 10).replace(/-/g, "_"); // format AAAA_MM_JJ
    const fileNameBase = `${dateString}_liste_${type}_${format.toUpperCase()}`;

    if (format === 'csv') {
        const csvContent = [headers, ...data]
            .map(row => row.map(val => `"${val.replace(/"/g, '""')}"`).join(","))
            .join("\n");
        const blob = new Blob(["\uFEFF" + csvContent], { type: "text/csv;charset=utf-8;" });
        download(`${fileNameBase}.csv`, blob);
    }

    if (format === 'json') {
        const jsonData = data.map(row =>
            Object.fromEntries(headers.map((key, i) => [key, row[i]]))
        );
        const blob = new Blob([JSON.stringify(jsonData, null, 2)], { type: "application/json" });
        download(`${fileNameBase}.json`, blob);
    }
}



function download(filename, blobContent) {
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blobContent);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}


$(document).ready(function(){
    let organismesLoaded = false;
    let formationsLoaded = false;

    $("#btnToggleOrganismes").click(function(){
        const table = $("#tableOrganismes");
        const btn = $("#btnToggleOrganismes");
        const exportBtn = $("#exportOrganismes");

        if (!organismesLoaded) {
            $.get("/organismes/all", function(response) {
                const tbody = table.find("tbody").empty();
                response.forEach(o => {
                    tbody.append(`
                        <tr id="organisme-row-${o.id}">
                            <td>${o.id}</td>
                            <td>${o.nom}</td>
                            <td>${o.adresse}</td>
                            <td>${o.email}</td>
                            <td>${o.telephone}</td>
                            <td><button class="btn btn-danger btn-sm" onclick="supprimerOrganisme(${o.id})">🗑</button></td>
                        </tr>
                    `);
                });
                $("#countOrganismes").text(response.length);
                table.show();
                exportBtn.show();
                btn.html('<i class="fas fa-eye-slash"></i> Cacher les organismes');
                organismesLoaded = true;
            });
        } else {
            const isVisible = table.is(":visible");
            if (isVisible) {
                table.hide();
                exportBtn.hide();
                btn.html('<i class="fas fa-eye"></i> Voir les organismes');
            } else {
                table.show();
                exportBtn.show();
                btn.html('<i class="fas fa-eye-slash"></i> Cacher les organismes');
            }
        }
    });

   $("#btnToggleFormations").click(function(){
        const table = $("#tableFormations");
        const btn = $("#btnToggleFormations");
        const exportBtn = $("#exportFormations");

        if (!formationsLoaded) {
            $.get("/formations/all", function(response) {
                const tbody = table.find("tbody").empty();
                response.forEach(f => {
                    tbody.append(`
                        <tr id="formation-row-${f.id}">
                            <td>${f.id}</td>
                            <td>${f.nom}</td>
                            <td>${f.type}</td>
                            <td>${f.description}</td>
                            <td>${f.duree}</td>
                            <td>${f.lieu}</td>
                            <td>${f.prix}</td>
                            <td><button class="btn btn-danger btn-sm" onclick="supprimerFormation(${f.id})">🗑</button></td>
                        </tr>
                    `);
                });
                $("#countFormations").text(response.length);
                table.show();
                exportBtn.show();
                btn.html('<i class="fas fa-eye-slash"></i> Cacher les formations');
                formationsLoaded = true;
            });
        } else {
            const isVisible = table.is(":visible");
            if (isVisible) {
                table.hide();
                exportBtn.hide();
                btn.html('<i class="fas fa-eye"></i> Voir les formations');
            } else {
                table.show();
                exportBtn.show();
                btn.html('<i class="fas fa-eye-slash"></i> Cacher les formations');
            }
        }
    });
});

// Supprime les flashs automatiquement après 5 secondes
document.addEventListener("DOMContentLoaded", () => {
    const flashMessages = document.querySelectorAll(".flash-popup");
    flashMessages.forEach((msg) => {
        setTimeout(() => {
            msg.style.display = "none";
        }, 4000);
    });
});


// Filtrage des formations
function filtrerFormations() {
    const search = $("#searchInput").val().toLowerCase();
    const type = $("#filterType").val();

    $("#tableFormations tbody tr").each(function () {
        const nom = $(this).find(".col-nom").text().toLowerCase();
        const organisme = $(this).find(".col-organisme").text().toLowerCase();
        const typeRow = $(this).find(".col-type").text().toLowerCase();

        const matchRecherche = nom.includes(search) || organisme.includes(search);
        const matchType = type === "" || typeRow === type;

        $(this).toggle(matchRecherche && matchType);
    });

    // Mise à jour du compteur
    const visibleRows = $("#tableFormations tbody tr:visible").length;
    $("#countFormations").text(`Total : ${visibleRows}`);
}

// Autocomplétion depuis API data.gouv
function activerAutoCompletion() {
    const $input = $("#searchInput");
    $input.on("input", function () {
        const query = $(this).val();
        if (query.length < 3) return;

        fetch(`https://recherche-entreprises.api.gouv.fr/search?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                const suggestions = data.results.slice(0, 5).map(r => r.nom_entreprise);
                // À toi d'intégrer un affichage de suggestions sous l'input
                console.log("Suggestions :", suggestions);
            });
    });
}

$(document).ready(() => {
    $("#searchInput, #filterType").on("input change", filtrerFormations);
    activerAutoCompletion();
});

// Gestion du bouton d'état
document.getElementById('etatBtn')?.addEventListener('click', function() {
    const currentState = this.getAttribute('data-state');
    const newState = currentState === 'valide' ? 'en_attente' : 'valide';
    this.setAttribute('data-state', newState);
    this.textContent = newState === 'valide' ? 'Validé' : 'En attente';
    document.getElementById('etatInput').value = newState;
});

// Gestion de la suppression
document.getElementById('deleteBtn')?.addEventListener('click', function() {
    document.getElementById('deleteModal').style.display = 'flex';
});

document.getElementById('cancelDelete')?.addEventListener('click', function() {
    document.getElementById('deleteModal').style.display = 'none';
});

// Fermer la modal si on clique en dehors
window.addEventListener('click', function(event) {
    const modal = document.getElementById('deleteModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

// === PAGE : preview_formation.html ===

// Gestion de l'état (bouton switch)
document.getElementById('etatBtn')?.addEventListener('click', function() {
    const newState = this.getAttribute('data-state') === 'valide' ? 'en_attente' : 'valide';
    this.setAttribute('data-state', newState);
    this.textContent = newState === 'valide' ? 'Validé' : 'En attente';
    document.getElementById('etatInput').value = newState;
});

// Gestion modal suppression
document.getElementById('deleteBtn')?.addEventListener('click', () => {
    document.getElementById('deleteModal').style.display = 'flex';
});

document.getElementById('cancelDelete')?.addEventListener('click', () => {
    document.getElementById('deleteModal').style.display = 'none';
});

window.addEventListener('click', function(event) {
    const modal = document.getElementById('deleteModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

// Ferme le modal si on clique à l'extérieur
window.addEventListener('click', function(event) {
    const modal = document.getElementById('deleteModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});


function openDeleteModal() {
    document.getElementById('deleteModal').style.display = 'flex';
}
function closeDeleteModal() {
    document.getElementById('deleteModal').style.display = 'none';
}

// === PAGE : dashboard.html ===

// Gestion des modals de raison

let currentAction = ''; // 'edit' ou 'delete'
let currentId = ''; // ID de la formation

$(document).ready(function () {
    // Cas 1 : depuis dashboard (suppression)
    $('.btn-delete').on('click', function (e) {
        e.preventDefault();
        currentAction = 'delete';
        currentId = $(this).data('id');
        $('#modalTitle').text("Raison de la suppression");
        $('#reasonText').val('');
        $('#reasonModal').show();
    });

    // Cas 2 : depuis formulaire modification (soumettre)
    $('#submitModification').on('click', function (e) {
        e.preventDefault();
        currentAction = 'edit';
        $('#modalTitle').text("Raison de la modification");
        $('#reasonText').val('');
        $('#reasonModal').show();
    });

    // Annuler
    $('#cancelReason').on('click', function () {
        $('#reasonModal').hide();
    });

    // Confirmer
    $('#confirmReason').on('click', function() {
        const reason = $('#reasonText').val().trim();
        if (!reason) {
            alert("Veuillez indiquer une raison.");
            return;
        }

        if (currentAction === 'delete') {
            const form = $('<form>', {
                'method': 'POST',
                'action': '/formations/delete_with_reason'
            }).append(
                $('<input>', {
                    'type': 'hidden',
                    'name': 'id',
                    'value': currentId
                }),
                $('<input>', {
                    'type': 'hidden',
                    'name': 'reason',
                    'value': reason
                })
            );

            $(document.body).append(form);
            form.submit();
        }

        $('#reasonModal').hide();
    });
}
);

// Gestion de la suppression
document.querySelectorAll('.delete-organisme').forEach(btn => {
    btn.addEventListener('click', function() {
        const id = this.getAttribute('data-id');
        if (confirm('Êtes-vous sûr de vouloir supprimer cet organisme ?')) {
            fetch(`/organismes/delete/${id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Supprimer la ligne du tableau
                        document.querySelector(`.organisme-row[data-id="${id}"]`).remove();
                        
                        // Afficher un message de succès
                        const flashContainer = document.getElementById('flashPopupContainer');
                        const flashMsg = document.createElement('div');
                        flashMsg.className = 'flash-popup flash-success';
                        flashMsg.innerHTML = 'Organisme supprimé avec succès!<span class="close-btn">&times;</span>';
                        flashContainer.appendChild(flashMsg);
                        
                        // Fermer le message après 5s
                        setTimeout(() => flashMsg.remove(), 5000);
                        
                        // Mettre à jour la pagination
                        updatePagination();
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    });
});

