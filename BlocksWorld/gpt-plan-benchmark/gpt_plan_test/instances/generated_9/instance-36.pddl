

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b i)
(on c a)
(on d g)
(on e f)
(on f h)
(on g b)
(on h d)
(ontable i)
(clear c)
(clear e)
)
(:goal
(and
(on b d)
(on c i)
(on d a)
(on e c)
(on g f)
(on h b)
(on i g))
)
)


