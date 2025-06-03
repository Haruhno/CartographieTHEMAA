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

document.addEventListener('DOMContentLoaded', function() {
    // Pagination pour les organismes
    if (document.getElementById('tableOrganismes')) {
        const organismeRows = document.querySelectorAll('#tableOrganismes .organisme-row');
        const itemsPerPageOrganismes = document.getElementById('itemsPerPageOrganismes');
        
        let currentPageOrganismes = 1;
        let itemsPerPageOrg = parseInt(itemsPerPageOrganismes.value);

        function updatePaginationOrganismes() {
            const totalPages = Math.ceil(organismeRows.length / itemsPerPageOrg) || 1;
            
            // Masquer toutes les lignes
            organismeRows.forEach(row => row.style.display = 'none');
            
            // Afficher les lignes de la page courante
            const startIndex = (currentPageOrganismes - 1) * itemsPerPageOrg;
            const endIndex = startIndex + itemsPerPageOrg;
            
            organismeRows.forEach((row, index) => {
                if (index >= startIndex && index < endIndex) {
                    row.style.display = '';
                }
            });

            // Mettre à jour les infos de pagination
            document.getElementById('pageInfoOrganismes').textContent = `Page ${currentPageOrganismes} sur ${totalPages}`;
            document.getElementById('pageInfoOrganismesBottom').textContent = `Page ${currentPageOrganismes} sur ${totalPages}`;
            document.getElementById('itemCountOrganismes').textContent = `Affichage de ${organismeRows.length} organismes`;
            document.getElementById('itemCountOrganismesBottom').textContent = `Affichage de ${organismeRows.length} organismes`;

            // Désactiver les boutons si nécessaire
            document.getElementById('prevPageOrganismes').disabled = currentPageOrganismes === 1;
            document.getElementById('prevPageOrganismesBottom').disabled = currentPageOrganismes === 1;
            document.getElementById('nextPageOrganismes').disabled = currentPageOrganismes === totalPages || totalPages === 0;
            document.getElementById('nextPageOrganismesBottom').disabled = currentPageOrganismes === totalPages || totalPages === 0;
        }

        // Événements pour la pagination des organismes
        itemsPerPageOrganismes.addEventListener('change', function() {
            itemsPerPageOrg = parseInt(this.value);
            currentPageOrganismes = 1;
            updatePaginationOrganismes();
        });

        document.getElementById('prevPageOrganismes').addEventListener('click', function() {
            if (currentPageOrganismes > 1) {
                currentPageOrganismes--;
                updatePaginationOrganismes();
            }
        });

        document.getElementById('nextPageOrganismes').addEventListener('click', function() {
            const totalPages = Math.ceil(organismeRows.length / itemsPerPageOrg);
            if (currentPageOrganismes < totalPages) {
                currentPageOrganismes++;
                updatePaginationOrganismes();
            }
        });

        document.getElementById('prevPageOrganismesBottom').addEventListener('click', function() {
            if (currentPageOrganismes > 1) {
                currentPageOrganismes--;
                updatePaginationOrganismes();
            }
        });

        document.getElementById('nextPageOrganismesBottom').addEventListener('click', function() {
            const totalPages = Math.ceil(organismeRows.length / itemsPerPageOrg);
            if (currentPageOrganismes < totalPages) {
                currentPageOrganismes++;
                updatePaginationOrganismes();
            }
        });

        // Initialisation
        updatePaginationOrganismes();
    }

    // Pagination pour les formations
    if (document.getElementById('tableFormations')) {
        const formationRows = document.querySelectorAll('#tableFormations .formation-row');
        const itemsPerPageFormations = document.getElementById('itemsPerPageFormations');
        
        let currentPageFormations = 1;
        let itemsPerPageForm = parseInt(itemsPerPageFormations.value);

        function updatePaginationFormations() {
            const totalPages = Math.ceil(formationRows.length / itemsPerPageForm) || 1;
            
            // Masquer toutes les lignes
            formationRows.forEach(row => row.style.display = 'none');
            
            // Afficher les lignes de la page courante
            const startIndex = (currentPageFormations - 1) * itemsPerPageForm;
            const endIndex = startIndex + itemsPerPageForm;
            
            formationRows.forEach((row, index) => {
                if (index >= startIndex && index < endIndex) {
                    row.style.display = '';
                }
            });

            // Mettre à jour les infos de pagination
            document.getElementById('pageInfoFormations').textContent = `Page ${currentPageFormations} sur ${totalPages}`;
            document.getElementById('pageInfoFormationsBottom').textContent = `Page ${currentPageFormations} sur ${totalPages}`;
            document.getElementById('itemCountFormations').textContent = `Affichage de ${formationRows.length} formations`;
            document.getElementById('itemCountFormationsBottom').textContent = `Affichage de ${formationRows.length} formations`;

            // Désactiver les boutons si nécessaire
            document.getElementById('prevPageFormations').disabled = currentPageFormations === 1;
            document.getElementById('prevPageFormationsBottom').disabled = currentPageFormations === 1;
            document.getElementById('nextPageFormations').disabled = currentPageFormations === totalPages || totalPages === 0;
            document.getElementById('nextPageFormationsBottom').disabled = currentPageFormations === totalPages || totalPages === 0;
        }

        // Événements pour la pagination des formations
        itemsPerPageFormations.addEventListener('change', function() {
            itemsPerPageForm = parseInt(this.value);
            currentPageFormations = 1;
            updatePaginationFormations();
        });

        document.getElementById('prevPageFormations').addEventListener('click', function() {
            if (currentPageFormations > 1) {
                currentPageFormations--;
                updatePaginationFormations();
            }
        });

        document.getElementById('nextPageFormations').addEventListener('click', function() {
            const totalPages = Math.ceil(formationRows.length / itemsPerPageForm);
            if (currentPageFormations < totalPages) {
                currentPageFormations++;
                updatePaginationFormations();
            }
        });

        document.getElementById('prevPageFormationsBottom').addEventListener('click', function() {
            if (currentPageFormations > 1) {
                currentPageFormations--;
                updatePaginationFormations();
            }
        });

        document.getElementById('nextPageFormationsBottom').addEventListener('click', function() {
            const totalPages = Math.ceil(formationRows.length / itemsPerPageForm);
            if (currentPageFormations < totalPages) {
                currentPageFormations++;
                updatePaginationFormations();
            }
        });

        // Initialisation
        updatePaginationFormations();
    }

    // Pour les cartes de formations utilisateur
    if (document.querySelector('.user-formations-grid')) {
        const formationCards = document.querySelectorAll('.user-formation-card');
        const itemsPerPageUser = 6; // 6 cartes par page
        let currentPageUser = 1;
        const totalPagesUser = Math.ceil(formationCards.length / itemsPerPageUser);

        function updateUserFormationsPagination() {
            // Masquer toutes les cartes
            formationCards.forEach(card => card.style.display = 'none');
            
            // Afficher les cartes de la page courante
            const startIndex = (currentPageUser - 1) * itemsPerPageUser;
            const endIndex = startIndex + itemsPerPageUser;
            
            formationCards.forEach((card, index) => {
                if (index >= startIndex && index < endIndex) {
                    card.style.display = '';
                }
            });

            // Créer ou mettre à jour les contrôles de pagination
            let paginationControls = document.querySelector('.user-formations-pagination');
            if (!paginationControls) {
                paginationControls = document.createElement('div');
                paginationControls.className = 'user-formations-pagination';
                document.querySelector('.user-formations-grid').after(paginationControls);
            }

            paginationControls.innerHTML = `
                <div class="pagination-buttons">
                    <button class="btn" id="prevPageUser" ${currentPageUser === 1 ? 'disabled' : ''}>
                        <i class="fas fa-chevron-left"></i> Précédent
                    </button>
                    <span>Page ${currentPageUser} sur ${totalPagesUser}</span>
                    <button class="btn" id="nextPageUser" ${currentPageUser === totalPagesUser ? 'disabled' : ''}>
                        Suivant <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            `;

            // Ajouter les événements
            document.getElementById('prevPageUser')?.addEventListener('click', () => {
                if (currentPageUser > 1) {
                    currentPageUser--;
                    updateUserFormationsPagination();
                }
            });

            document.getElementById('nextPageUser')?.addEventListener('click', () => {
                if (currentPageUser < totalPagesUser) {
                    currentPageUser++;
                    updateUserFormationsPagination();
                }
            });
        }

        // Initialisation
        if (formationCards.length > itemsPerPageUser) {
            updateUserFormationsPagination();
        }
    }
});

