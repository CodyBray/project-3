#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 14:34:19 2021

@author: kendrick
"""

import numpy as np

# compute unknown displacements 
def ComputeDisplacements(K, F, n_unknowns):
    # extract submatrix of unknowns
    K11 = K[0:n_unknowns,0:n_unknowns]
    F1 = F[0:n_unknowns]
    
    d = np.linalg.solve(K11,F1)
    
    return d

# postprocess the forces at known displacement nodes
def PostprocessReactions(K, d, F, n_unknowns, nodes):
    # These are computed net forces and do not
    # take into account external loads applied
    # at these nodes
    F = np.matmul(K[n_unknowns:,0:n_unknowns], d)
    
    # Postprocess the reactions
    for node in nodes:
        if node.xidx >= n_unknowns:
            node.AddReactionXForce(F[node.xidx-n_unknowns][0] - node.xforce_external)
        if node.yidx >= n_unknowns:
            node.AddReactionYForce(F[node.yidx-n_unknowns][0] - node.yforce_external)
        
    return F

# determine internal member loads
def ComputeMemberForces(bars):
    # COMPLETE THIS FUNCTION
    #iterate 
    for bar in bars:
    #define terms
        E= bar.E
        A= bar.A
        L=bar.Length()
        lambdax,lambday = bar.LambdaTerms()
        lambdamatrix=np.array([-lambdax,-lambday,lambdax,lambday])
        node_1=bar.init_node
        node_2=bar.end_node
        d1x=node_1.xdisp
        d1y=node_1.ydisp
        d2x=node_2.xdisp
        d2y=node_2.ydisp
        Dmatrix=np.array([d1x,d1y,d2x,d2y])
       
 # Compute member forces for all bars using equation 14-23 
        Qf=A*E/L*np.dot(lambdamatrix,Dmatrix)
        bar.axial_load=Qf

        #self.axial_load = float("NAN")   
        
# compute the normal stresses
def ComputeNormalStresses(bars):
    # COMPLETE THIS FUNCTION
    # Compute normal stress for all bars
    for bar in bars:
        a=bar.A
        f=bar.axial_load
        stress=f/a
        bar.normal_stress = stress


# compute the critical buckling load of a member
def ComputeBucklingLoad(bars):
    # COMPLETE THIS FUNCTION
    # Compute critical buckling load for all bars
    for bar in bars :
        E=bar.E
        I=bar.It
        Pcr= np.pi**2*E*I/(1*bar.Length())**2
        bar.buckling_load = Pcr