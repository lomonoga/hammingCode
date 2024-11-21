def encoder(input_data: str):
    # Инвертируем входные данные для работы с младших битов
    reversed_data = list(input_data)
    reversed_data.reverse()
    control_bit_index, current_parity_index, data_index, redundant_bit_count = 0, 0, 0, 0
    encoded_data = []

    # Определяем количество проверочных (контрольных) битов
    while (len(input_data) + redundant_bit_count + 1) > (2 ** redundant_bit_count):
        redundant_bit_count += 1

    # Заполняем список контрольных битов и данных
    for bit_position in range(redundant_bit_count + len(reversed_data)):
        if (2 ** control_bit_index) == (bit_position + 1):  # Если позиция битов - степень двойки
            encoded_data.append(0)  # Добавляем контрольный бит (пока 0)
            control_bit_index += 1
        else:
            encoded_data.append(int(reversed_data[data_index]))
            data_index += 1

    # Заполняем контрольные биты, проходясь по данным
    for parity_bit_position in range(len(encoded_data)):
        parity_position = (2 ** current_parity_index)
        if (parity_bit_position + 1) == parity_position:
            start_index = parity_position - 1
            current_index = start_index
            xor_block = []

            while current_index < len(encoded_data):
                block = encoded_data[current_index:current_index + parity_position]
                xor_block.extend(block)
                current_index += 2 * parity_position

            # Применяем XOR для всех блоков, чтобы вычислить контрольный бит
            for bit in range(1, len(xor_block)):
                encoded_data[start_index] ^= xor_block[bit]
            current_parity_index += 1

    encoded_data.reverse()  # Инвертируем обратно для получения результата
    return ''.join(map(str, encoded_data))


def decoder(input_data: str):
    # Инвертируем входные данные для работы с младших битов
    reversed_data = list(input_data)
    reversed_data.reverse()
    control_bit_index, current_parity_index, data_index = 0, 0, 0
    error_position = 0
    data_with_control_bits, parity_results, corrected_data = [], [], []

    # Восстанавливаем данные с контрольными битами
    for bit_position in range(len(reversed_data)):
        if (2 ** control_bit_index) == (bit_position + 1):
            control_bit_index += 1
        data_with_control_bits.append(int(reversed_data[bit_position]))
        corrected_data.append(reversed_data[bit_position])

    # Проверяем наличие ошибок
    for parity_bit_position in range(len(data_with_control_bits)):
        parity_position = (2 ** current_parity_index)
        if parity_position == (parity_bit_position + 1):
            start_index = parity_position - 1
            current_index = start_index
            xor_block = []

            while current_index < len(data_with_control_bits):
                block = data_with_control_bits[current_index:current_index + parity_position]
                xor_block.extend(block)
                current_index += 2 * parity_position

            # Применяем XOR для проверки
            for bit in range(1, len(xor_block)):
                data_with_control_bits[start_index] ^= xor_block[bit]
            parity_results.append(data_with_control_bits[parity_bit_position])
            current_parity_index += 1

    # Вычисляем ошибочную позицию
    parity_results.reverse()
    error_position = sum(
        int(parity_results[bit]) * (2 ** bit) for bit in range(len(parity_results))
    )

    # Исправляем ошибку, если она есть
    if 0 < error_position <= len(corrected_data):
        print(f'Error detected at bit position: {error_position}')
        corrected_data[error_position - 1] = '1' if corrected_data[error_position - 1] == '0' else '0'

    # Удаляем контрольные биты
    control_bit_index = 0
    decoded_data = []
    for bit_position in range(len(corrected_data)):
        if (bit_position + 1) != (2 ** control_bit_index):
            decoded_data.append(corrected_data[bit_position])
        else:
            control_bit_index += 1

    decoded_data.reverse()  # Инвертируем обратно для результата
    return ''.join(map(str, decoded_data))


input_data = input('Enter a string to encode: ')

encoder_data = encoder(input_data)
print(f'Encoder Data: {encoder_data}')

decoder_data = decoder(encoder_data)
print(f'Encoder Data: {decoder_data}')
