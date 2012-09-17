import numpy

def simulate(cmodel, dr, s0, sigma, n_exp=0, horizon=40, with_auxiliaries=True, parms=None, seed=1, discard=False,):

    '''
    :param cmodel: 
    :param dr:
    :param s0:
    :param sigma:
    :param n_exp:
    :param horizon:
    :param with_auxiliaries:
    :param parms:
    :param seed:
    :param discard:
    :return:
    '''

    cmodel = cmodel.as_type('fg')

    if n_exp ==0:
        irf = True
        n_exp = 1
    else:
        irf = False

    from dolo.symbolic.model import Model
    if isinstance(cmodel,Model):
        from dolo.compiler.compiler_global import GlobalCompiler
        model = cmodel
        cmodel = GlobalCompiler(model)
        [y,x,parms] = model.read_calibration()

    if parms == None:
        parms = cmodel.model.read_calibration()[2]


    s0 = numpy.atleast_2d(s0.flatten()).T

    x0 = dr(s0)

    s_simul = numpy.zeros( (s0.shape[0],n_exp,horizon) )
    x_simul = numpy.zeros( (x0.shape[0],n_exp,horizon) )

    s_simul[:,:,0] = s0
    x_simul[:,:,0] = x0

    for i in range(horizon):
        mean = numpy.zeros(sigma.shape[0])
        if irf:
            epsilons = numpy.zeros( (sigma.shape[0],1) )
        else:
            seed += 1
            numpy.random.seed(seed)
            epsilons = numpy.random.multivariate_normal(mean, sigma, n_exp).T
        s = s_simul[:,:,i]
        x = dr(s)
        x_simul[:,:,i] = x

        ss = cmodel.g(s,x,epsilons,parms)

        if i<(horizon-1):
            s_simul[:,:,i+1] = ss

    from numpy import any,isnan,all

    if not with_auxiliaries:
        simul = numpy.row_stack([s_simul, x_simul])
    else:
        a_simul = cmodel.a( s_simul.reshape((-1,n_exp*horizon)), s_simul.reshape( (-1,n_exp*horizon) ), parms)
        a_simul = a_simul.reshape(-1,n_exp,horizon)
        simul = numpy.row_stack([s_simul, x_simul, a_simul])

    if discard:
        iA = -isnan(x_simul)
        valid = all( all( iA, axis=0 ), axis=1 )
        simul = simul[:,valid,:]
        n_kept = s_simul.shape[1]
        if n_exp > n_kept:
            print( 'Discarded {}/{}'.format(n_exp-n_kept,n_exp))

    if irf:
        simul = simul[:,0,:]

    return simul


from dolo.misc.decorators import deprecated

@deprecated
def simulate_without_aux(cmodel, dr, s0, sigma, *args, **vargs):
    vargs['with_auxiliaries'] = False
    return simulate(cmodel, dr, s0, sigma, *args, **vargs)

if __name__ == '__main__':
    from dolo import yaml_import, approximate_controls
    model = yaml_import('../../../examples/global_models/capital.yaml')
    dr = approximate_controls(model)

    [y,x,parms] = model.read_calibration()
    sigma = model.read_covariances()

    from dolo.compiler.compiler_global import GlobalCompiler2

    import numpy
    cmodel = GlobalCompiler2(model)
    s0 = numpy.atleast_2d( dr.S_bar ).T

#    [s_simul, x_simul, a_simul] = simulate(cmodel, dr, s0, sigma, 10000, 50, parms, with_auxiliaries=True)
    simul = simulate(cmodel, dr, s0, sigma, 10000, 50)
    sim = simulate_without_aux(cmodel, dr, s0, sigma, 10000, 50)
    print(simul.shape)
    print sim.shape


    from matplotlib.pyplot import hist, show, figure


    timevec = numpy.array(range(simul.shape[2]))

    figure()
    for i in range( 50 ):
        hist( simul[0,:,i], bins=50 )
    show()
    #plot(timevec,s_simul[0,0,:])
