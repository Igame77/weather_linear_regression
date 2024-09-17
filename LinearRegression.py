class LinearRegression:
    def __init__(self) -> None:
        # y = k*x + m
        self.k = 0
        self.error = []
        self.m = 0
    
    def learn(self,x,y,epochs = 20):
        self.m = y[0] - 1
        
        for j in range(epochs):
            for i in range(len(x)):
                self.k += x[i] * (y[i] - self.m)
            
            self.k /= sum(el ** 2 for el in x)
            self.error = [y[i]- x[i] * self.k - self.m for i in range(len(x))]
            self.m += sum(self.error) / len(self.error)
        
    
    def predict(self, x):
        return self.k * x - self.m
            

    def clear_data(self):
        self.k, self.error, self.m = 0, 0, 0

