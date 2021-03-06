import numpy as np
from collections import deque
import random
from keras.models import Sequential,Model
from keras.layers import Dropout,Dense,Input,Activation
from keras.optimizers import Adam

class Elon_Musk:
    def __init__(self,nx,ny,lr,gamma):
        self.nx = nx
        self.ny = ny
        self.lr = lr
        self.los = []
        self.gamma = gamma
        self.memory_deck = deque(maxlen=2000)
        self.epsilon = 0.7
        self.epsilon_ = 0.01
        self.dc = 0.995
        self.model = self.get_model()
        self.episode_observation, self.episode_rewards, self.episode_action, self.new_episode_observation,self.episode_flag = [],[],[],[],[]

    def get_model(self):
        model = Sequential()
        model.add(Dense(128,input_dim=self.nx,activation='relu'))
        model.add(Dense(128,activation='relu'))
        model.add(Dense(self.ny,activation='linear'))
        model.compile(loss='mse',optimizer=Adam(lr=self.lr))
        return model

    def get_action(self,observation):
        if np.random.rand()<=self.epsilon:
            return np.random.choice(len(range(4)))
        p = self.model.predict(observation)
        action = np.argmax(p[0])
        return action
    
    def memory_recall(self,observation,action,reward,new_observation,flags):
        self.memory_deck.append((observation,action,reward,new_observation,flags))
        self.episode_rewards.append(reward)

    def training(self,batch):
        i = random.sample(self.memory_deck,batch)
        self.los = []
        for obs,act,rew,new_obs,done in i:
            target = rew
            if not done:
                target = ((1.0-0.1)*rew+0.1*(self.gamma*np.amax(self.model.predict(new_obs)[0])))
            
            old_target = self.model.predict(obs)
            old_target[0][act] = target
            history = self.model.fit(x=obs,y=old_target,verbose=0,epochs=1)
            self.los.append(history.history['loss'])
            self.episode_observation, self.episode_rewards, self.episode_action, self.new_episode_observation,self.episode_flag = [],[],[],[],[]

        mm = np.mean(self.los)
        if self.epsilon>=self.epsilon_:
            self.epsilon*=self.dc
        return history,mm


        



