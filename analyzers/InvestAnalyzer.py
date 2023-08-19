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
      
      for row in data:
         
         tech_analysis_data.append(row[-1])
         row.pop(-1)
      
      maxValues = [*data[0]]
      minValues = [*data[0]]
      
      if len(data) > 1:
         for i, row in enumerate(data, 1):
            for j in range(len(row)):
               
               if maxValues[j] < row[j]:
                  maxValues[j] = row[j]
               
               if minValues[j] > row[j]:
                  minValues[j] = row[j]
      
      averageValues = []
      
      for i, maxValue in enumerate(maxValues):
         averageValues.append((maxValue + minValues[i])/2)
      
      preMaxValues = []
      
      for i, maxValue in enumerate(maxValues):
         preMaxValues.append((maxValue + averageValues[i])/2)
         
      preMinValues = []
      
      for i, minValue in enumerate(minValues):
         preMinValues.append((minValue + averageValues[i])/2)
      
      for row in data:
         for i in range(len(row)):
            
            if row[i] >= maxValues[i] * 0.9:
               row[i] = 'best'
               continue
            
            if row[i] >= preMaxValues[i] * 0.9 and row[i] < maxValues[i] * 0.9:
               row[i] = 'good'
               continue
            
            if row[i] >= averageValues[i] * 1.1 and row[i] < preMaxValues[i] * 0.9:
               row[i] = 'neutral'
               continue
            
            if row[i] <= averageValues[i] * 0.9 and row[i] > minValues[i] * 1.1:
               row[i] = 'bad'
               continue
            
            if row[i] <= minValues[i] * 1.1:
               row[i] = 'worst'
               continue
      
      for i, item in enumerate(tech_analysis_data):
         data[i].append(InvestAnalyzer.tech_analysis_dict[item])
      
      return data
      
      
      
      
      