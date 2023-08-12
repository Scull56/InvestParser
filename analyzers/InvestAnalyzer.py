class InvestAnalyzer():
   
   tech_analysis_dict = {
      "Strong Buy": "best",
      "Buy": "good",
      "Neutral": "neutral",
      "Sell": "bad",
      "Strong Sell": "worst"
   }
      
   def analyze(self, data):
      
      tech_analysis_data = []
      
      for item in data:
         
         tech_analysis_data.append(item[-1])
         data.pop(-1)
      
      maxValues = [data[0]]
      minValues = [data[0]]
      
      for i, row in enumerate(data, 1):
         for j in range(len(row)):
         
            if maxValues[i][j] < row[j]:
               maxValues[i][j] = row[j]
            
            if minValues[i][j] > row[j]:
               minValues[i][j] = row[j]
      
      averageValues = []
      
      for i, maxValue in enumerate(maxValues):
         averageValues.append((maxValue + minValues[i])/2)
      
      preMaxValues = []
      
      for i, maxValue in enumerate(maxValues):
         preMaxValues.append((maxValue + averageValues[i])/2)
         
      preMinValues = []
      
      for i, minValue in enumerate(minValues):
         preMinValues.append((minValue + averageValues[i])/2)
      
      
      
      
      
      
      