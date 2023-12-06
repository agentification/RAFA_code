

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a c)
(on b i)
(on c d)
(on d g)
(ontable e)
(on f e)
(on g h)
(ontable h)
(ontable i)
(clear a)
(clear b)
(clear f)
)
(:goal
(and
(on a e)
(on d f)
(on e c)
(on f h)
(on g b)
(on h g)
(on i d))
)
)


