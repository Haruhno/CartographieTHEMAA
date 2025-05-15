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
                table.slideDown();
                exportBtn.slideDown();
                btn.html('<i class="fas fa-eye-slash"></i> Cacher les organismes');
                organismesLoaded = true;
            });
        } else {
            table.slideToggle();
            exportBtn.slideToggle();
            const isVisible = table.is(":visible");
            btn.html(isVisible
                ? '<i class="fas fa-eye-slash"></i> Cacher les organismes'
                : '<i class="fas fa-eye"></i> Voir les organismes');
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
                table.slideDown();
                exportBtn.slideDown();
                btn.html('<i class="fas fa-eye-slash"></i> Cacher les formations');
                formationsLoaded = true;
            });
        } else {
            table.slideToggle();
            exportBtn.slideToggle();
            const isVisible = table.is(":visible");
            btn.html(isVisible
                ? '<i class="fas fa-eye-slash"></i> Cacher les formations'
                : '<i class="fas fa-eye"></i> Voir les formations');
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

