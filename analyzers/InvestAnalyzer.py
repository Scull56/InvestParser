class InvestAnalyzer():
   
   tech_analysis_dict = {
      "Strong Buy": "best",
      "Buy": "good",
      "Neutral": "neutral",
      "Sell": "bad",
      "Strong Sell": "worst"
   }
   
   def __init__(self, mode_list):
      self.mode_list = mode_list
      
   def analyze(self, data):

      for row in data:
         for i in range(len(row)):
            if self.mode_list[i] == 'near_zero':
               row[i] = 1 / row[i]

      maxValues = [*data[0]]
      minValues = [*data[0]]
      
      if len(data) > 1:
         for i, row in enumerate(data, 1):
            for j in range(len(row)):
               
               if self.mode_list[j] != 'value':
                  if maxValues[j] < row[j]:
                     maxValues[j] = row[j]
                  
                  if minValues[j] > row[j]:
                     minValues[j] = row[j]
               else:
                  maxValues[j] = ''
                  minValues[j] = ''
      
      averageValues = []

      for i, maxValue in enumerate(maxValues):
         
         if self.mode_list[i] != 'value':
            averageValues.append((maxValue + minValues[i])/2)
            
         else:
            averageValues.append('')
      
      for row in data:
         for i in range(len(row)):
            
            if self.mode_list[i] in ['near_zero', 'more']:
            
               row[i] = self.get_definer(row[i], maxValues[i], minValues[i], averageValues[i], 'more')
            
            if self.mode_list[i] == 'less':
               
               row[i] = self.get_definer(row[i], maxValues[i], minValues[i], averageValues[i], 'less')
            
            if self.mode_list[i] == 'value':
               
               row[i] = InvestAnalyzer.tech_analysis_dict[row[i]]
      
      return data
      
   def get_definer(self, value, max, min, avarage, mode):
      
      if max == min:
         return 'best'
      
      maxBorder = max * 0.8 if max > 0 else max * 1.2
      avarageTop = avarage * 1.1 if avarage > 0 else avarage * 0.9
      avarageBottom = avarage * 0.9 if avarage > 0 else avarage * 1.1
      minBorder = min * 1.2 if min > 0 else min * 0.8
      
      if value >= maxBorder:
         return 'best' if mode == 'more' else 'worst'
      
      if value >= avarageTop and value < maxBorder:
         return 'good' if mode == 'more' else 'bad'
      
      if value >= avarageTop and value < avarageBottom:
         return 'neutral'
      
      if value <= avarageBottom and value > minBorder:
         return 'bad' if mode == 'more' else 'good'
      
      if value <= minBorder:
         return 'worst' if mode == 'more' else 'best'