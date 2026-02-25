let meuNome = prompt("Digite seu nome:");

function carregar() {

    fetch("/listar")
    .then(res => res.json())
    .then(dados => {

        let tabela = "";

        dados.forEach(item => {

            tabela += `
                <tr>
                    <td>${item.nome || ""}</td>
                    <td>${item.numero || ""}</td>
                    <td>${item.email || ""}</td>
                    <td>${item.historico || ""}</td>
                    <td>${item.tipo || ""}</td>
                    <td>${item.link || ""}</td>
                    <td>${item.imovel || ""}</td>
                    <td>${item.data_criacao || ""}</td>
                    <td>${item.canal || ""}</td>
                    <td>${item.status}</td>
                    <td>${item.atendimento || ""}</td>
                    <td>${item.detalhes || ""}</td>
                    <td>${item.atendente || "-"}</td>
                    <td>
                        ${item.status === "Aguardando" ?
                        `<button onclick="assumir(${item.id})">Assumir</button>` : ""}
                    </td>
                </tr>
            `;
        });

        document.getElementById("lista").innerHTML = tabela;
    });
}

function assumir(id) {

    fetch("/assumir/" + id, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({atendente: meuNome})
    }).then(() => carregar());
}

carregar();
setInterval(carregar, 5000);
