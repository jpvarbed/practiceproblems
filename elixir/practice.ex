defmodule Detector do
  def better_than_average(class_points, your_points) do
    your_points > Enum.reduce(class_points, fn (score, sum) -> sum + score end) / length(class_points)
  end
end

defmodule Shepherd do
  def count_sheeps([]), do: 0
  def count_sheeps(sheeps) when not is_list(sheeps), do: 0
  def count_sheeps(sheeps) do
    #initial acc value, fn with  element and accumulator
    Enum.reduce(sheeps, 0, fn (sheepValue, sheep) ->
      if sheepValue, do: sheep + 1, else: sheep
    end)
  end
end

# defmodule Shepherd do
#   def count_sheeps(sheeps) do
#     Enum.count(sheeps, &(&1))
#   end
# end

defmodule StringUtils do
  def upper_case?(str) do
    String.equivalent?(str, String.upcase(str))
    # !Regex.match?(~r/[a-z]/, str)
  end
end


defmodule Codewars.StringUtils do
  @d ?a - ?A

  def alter_case(str) do
    str
    |> String.to_char_list
    |> Enum.map(&( _alter(&1)) )
    |> List.to_string
  end

  defp _alter(c) when c in ?a..?z, do: c - @d
  defp _alter(c) when c in ?A..?Z, do: c + @d
  defp _alter(c), do: c
end

# defmodule Codewars.StringUtils do
#   def alter_case(str) do
#     import String
#     import Enum

#     str
#     |> codepoints
#     |> map(&(if &1 == upcase(&1), do: downcase(&1), else: upcase(&1)))
#     |> to_string
#   end
# end

defmodule Codewars do
  def even_or_odd(number) do
  import Integer
    if Integer.is_even(number) do
      "Even"
    else
     "Odd"
    end
  end
end

# defmodule Codewars do
#   def even_or_odd(number) when rem(number, 2) == 0, do: "Even"
#   def even_or_odd(_), do: "Odd"
# end
