text = "X-DSPAM-Confidence:    0.8475"

colon_index = text.find(':')
value_str = text[colon_index+1:].strip()
value_float = float(value_str)

print(value_float)