

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b i)
(on c d)
(on d e)
(on e a)
(ontable f)
(on g h)
(on h b)
(ontable i)
(clear c)
(clear f)
(clear g)
)
(:goal
(and
(on b c)
(on c d)
(on d e)
(on f h)
(on g b)
(on h i)
(on i g))
)
)


