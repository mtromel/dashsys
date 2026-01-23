document.addEventListener('DOMContentLoaded', function() {
    const tipoField = document.querySelector('#id_tipo'); // ID do campo Tipo na Máquina
    
    function toggleFieldsets() {
        const tipo = tipoField.value;
        // No Django Admin, os fieldsets ganham classes baseadas na ordem ou título
        // Vamos buscar pelos títulos que você definiu
        const fieldsetDobradeira = document.querySelector('.group-especifico-dobradeira');
        const fieldsetLaser = document.querySelector('.group-especifico-laser');

        if (tipo === 'LASER') {
            if(fieldsetDobradeira) fieldsetDobradeira.style.display = 'none';
            if(fieldsetLaser) fieldsetLaser.style.display = 'block';
        } else if (tipo === 'DOBRADEIRA') {
            if(fieldsetDobradeira) fieldsetDobradeira.style.display = 'block';
            if(fieldsetLaser) fieldsetLaser.style.display = 'none';
        } else {
            // Se estiver vazio, esconde ambos para limpar a tela
            if(fieldsetDobradeira) fieldsetDobradeira.style.display = 'none';
            if(fieldsetLaser) fieldsetLaser.style.display = 'none';
        }
    }

    if (tipoField) {
        tipoField.addEventListener('change', toggleFieldsets);
        toggleFieldsets(); // Executa ao carregar para máquinas já existentes
    }
});