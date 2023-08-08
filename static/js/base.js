$(document).ready(function(){
	/* colapse */
	if ($('#bin_colaps').val())
	{
		if ($('#bin_colaps').val() <= 0)
		{
			var bin_colaps = "0";
		}
		else
		{
			var bin_colaps = "1";
		}
	}
	else
	{
		var bin_colaps = "0";
	}

	/* mascaras **/
	$('.money').mask("###.###.##0,00", {reverse: true});
	$('.margem').mask("##,00", {reverse: false});

	/* funções */

	function poemVirgula(x)
	{
		y = String(x).replace('.', ',');
		return y;
	}


	function atualizaValorFinal()
	{
		var valor_fornecedor = ($('#id_valor_fornecedor').cleanVal())/100;
		valor_fornecedor = Number(valor_fornecedor).toFixed(2);

		var valor_final = ($('#id_valor_final').cleanVal())/100;
		valor_final = Number(valor_final).toFixed(2);
		var margem = ($('#id_margem').cleanVal())/100;
		margem = Number(margem).toFixed(2);
		valor_final = (valor_fornecedor * (
                          100/ margem
                          )) / ((
                          100 / margem)-1);
        valor_final = valor_final.toFixed(2);
        $('#id_valor_final').val(poemVirgula(valor_final));
        $('.money').mask("###.###.##0,00", {reverse: true});
		$('.margem').mask("##,00", {reverse: false});
	}


	function atualizaMargem()
	{
		var valor_fornecedor = ($('#id_valor_fornecedor').cleanVal())/100;
		valor_fornecedor = Number(valor_fornecedor).toFixed(2);

		var valor_final = ($('#id_valor_final').cleanVal())/100;
		valor_final = Number(valor_final).toFixed(2);
		var margem = ($('#id_margem').cleanVal())/100;
		margem = Number(margem).toFixed(2);
		margem_final = 100 - ((valor_fornecedor ) / (
                          valor_final / 100));
        margem_final = margem_final.toFixed(2);
        $('#id_margem').val(poemVirgula(margem_final));
        $('.money').mask("###.###.##0,00", {reverse: true});
		$('#id_margem').mask("##,00", {reverse: false});
	}

	function trocaInfo()
	{
		if (bin_colaps == "1")
		{
			$('#a_mais_info').html("[Mais informações]");
			bin_colaps = 0;
		}
		else
		{
			$('#a_mais_info').html("[Menos informações]");
			bin_colaps = 1;
		}
		
	}


	/* ações */

	$('.atualiza_valor #id_valor_fornecedor').blur(function(){
		atualizaValorFinal();
	});


	$('.atualiza_valor #id_margem').blur(function(){
		atualizaValorFinal();
	});


	$('.atualiza_valor #id_valor_final').blur(function(){
		atualizaMargem();
	});

	$('#form-produto').on('keydown', function(event) {
    	if (event.key === 'Enter') {
        	event.preventDefault();
      	}
    });
	$('#form-produto').on('submit', function(event)
	{
		atualizaMargem();

		$('.money').unmask();
		$('.margem').unmask();
		valor_fornecedor = ($('#id_valor_fornecedor').val())/100;
		$('#id_valor_fornecedor').val(valor_fornecedor);
		valor_final = ($('#id_valor_final').val())/100;
		$('#id_valor_final').val(valor_final);
		if ($('#id_margem').val().length <= 2)
		{
			margem = $('#id_margem').val().toFixed(2);
		}
		margem = ($('#id_margem').val())/100;
		$('#id_margem').val(margem);
	});
	$('.filtro-orcamento').change(function()
	{
		$('#forminho').submit();
	});
	$('#a_mais_info').click(function(){
		trocaInfo();
	})
});