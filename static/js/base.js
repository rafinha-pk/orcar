$(document).ready(function(){
	/* - mascaras - */
	/*$('.money').mask("##0,00", {reverse: true});
	$('#id_margem').mask('##0,00', {reverse: true});*/

	/* - funções - */
	function LimpaMascara(valor)
	{
		/*limpo = valor.replace('.', '');*/
		var limpo = String(valor).replace(',', '.');
		limpo = parseInt(limpo);
		/*limpo = limpo.toFixed(2);*/
		return limpo;
	}
	function CriaMascara(valor)
	{
		var limpo = String(valor).replace('.', ',');
		limpo = parseInt(limpo)
		return limpo;
	}
	function AtualizaFinal(valor_fornecedor, margem)
	{
		margem = LimpaMascara(margem);
		valor_fornecedor = LimpaMascara(valor_fornecedor);
		valor_final = (valor_fornecedor * (
                          100/ margem
                          )) / ((
                          100 / margem)-1);
        valor_final = CriaMascara(valor_final).toFixed(2);
        margem = CriaMascara(margem).toFixed(2);
        valor_fornecedor = CriaMascara(valor_fornecedor).toFixed(2);
        $('#id_valor_fornecedor').val(valor_fornecedor);
        $('#id_margem').val(margem);
        $('#id_valor_final').val(valor_final);
	}

	function AtualizaMargem(valor_fornecedor, valor_final)
	{
		valor_fornecedor = LimpaMascara(valor_fornecedor);
		valor_final = LimpaMascara(valor_final);
		margem_final = 100 - ((valor_fornecedor ) / (
                          valor_final / 100));
		valor_final = CriaMascara(valor_final.toFixed(2));
        margem = CriaMascara(margem_final.toFixed(2));
        valor_fornecedor = CriaMascara(valor_fornecedor.toFixed(2));
        $('#id_valor_fornecedor').val(valor_fornecedor);
        $('#id_margem').val(margem);
        $('#id_valor_final').val(valor_final);
	}
	/* - ações - */ 
	$('.atualiza_valor #id_valor_fornecedor').change( function(){
											 AtualizaFinal(
											 			$('#id_valor_fornecedor').val(),
											 			$('#id_margem').val() );
		});
	$('.atualiza_valor #id_margem').change( function(){
											 AtualizaFinal(
											 			$('#id_valor_fornecedor').val(),
											 			$('#id_margem').val() );
		});
	$('.atualiza_valor #id_valor_final').change( function(){
										AtualizaMargem(
													$('#id_valor_fornecedor').val(),
											 		$('#id_valor_final').val() );
		});
});