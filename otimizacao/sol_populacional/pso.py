
def movimenta_particulas(particulas, indLider):

    for i in range(len(particulas)):
        if(i != indLider):
            (diff_particulas,menor_insta_particula) = compara_diff_solucoes(particulas[i],particulas[indLider])
        
        print(diff_particulas)
        print(menor_insta_particula)