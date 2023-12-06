

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b f)
(on c a)
(on d b)
(on e d)
(ontable f)
(on g i)
(on h e)
(ontable i)
(clear c)
(clear g)
(clear h)
)
(:goal
(and
(on a f)
(on b i)
(on c a)
(on d g)
(on f e)
(on g b))
)
)


