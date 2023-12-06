

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a h)
(on b i)
(on c g)
(ontable d)
(ontable e)
(on f c)
(on g b)
(on h d)
(ontable i)
(clear a)
(clear e)
(clear f)
)
(:goal
(and
(on a g)
(on c a)
(on d f)
(on f b)
(on h i)
(on i e))
)
)


